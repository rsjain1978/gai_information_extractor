$(document).ready(function() {
    $("#upload-form").submit(function(e) {
        e.preventDefault();
        let file = $("#pdf-upload")[0].files[0];
        let formData = new FormData();
        formData.append("file", file);
        
        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
                // Add spinner
            },
            success: function(data) {
                // Remove spinner
                $("#pdf-viewer").attr("src", URL.createObjectURL(file)).show();
                $("#company-dropdown").empty().append('<option value="">Select a company</option>');

                data.companies.forEach(function(company) {
                    $("#company-dropdown").append('<option value="' + company + '">' + company + '</option>');
                });

                $("#company-dropdown").show();
            }
        });
    });

    $("#company-dropdown").change(function() {
        let companyName = $(this).val();
        if (!companyName) return;

        $.ajax({
            url: "/analyse",
            type: "POST",
            data: { company: companyName },
            beforeSend: function() {
                // Add spinner
            },
            success: function(data) {
                // Remove spinner
                displayAnalysisResults(data);
            }
        });
    });
});

function displayAnalysisResults(data) {
    // Create the accordion content
    let accordionContent = "";
    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            // Split the text by the '\n' character to create a list
            const listItems = data[key].split('\n').map(item => `<li>${item}</li>`).join('');
            accordionContent += `
                <h3>${key}</h3>
                <div>
                    <ul>${listItems}</ul>
                </div>
            `;
        }
    }

    // Destroy the existing accordion (if any) before adding new content
    if ($("#accordion").hasClass("ui-accordion")) {
        $("#accordion").accordion("destroy");
    }

    // Add the content to the accordion and initialize it
    $("#accordion").html(accordionContent).accordion({
        collapsible: true,
        active: false,
        heightStyle: "content",
    });

    // Show the analysis results container
    $("#analysis-results").show();
}
