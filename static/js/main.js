$(function () {
    var requiredInputFields = $("form.register input[type='text'][required='required'], form.register input[type='email'][required='required']");
    var requiredCheckboxFields = $("form.register input[type='checkbox'][required='required']");
    var requiredRadioFields = $("form.register input[type='radio'][required='required']");
    var requiredFieldCount = requiredInputFields.length + requiredCheckboxFields.length + requiredRadioFields.length;


    function validateLicenseId(jsonLicenseIdFormats, licenseId) {
        var validLicenseId = false;
        var regexLetter = /^[a-zA-Z]$/;
        var regexNumber = /^[0-9]$/;
        for (var i = 0; i < jsonLicenseIdFormats.length; i++) {
            if (jsonLicenseIdFormats[i].length == licenseId.length) {
                var alphaNumericMatch = true;
                for (var j = 0; j < jsonLicenseIdFormats[i].length; j++) {
                    if (!((regexLetter.test(jsonLicenseIdFormats[i][j]) && regexLetter.test(licenseId[j]))
                        || (regexNumber.test(jsonLicenseIdFormats[i][j]) && regexNumber.test(licenseId[j])))) {
                        alphaNumericMatch = false;
                        break;
                    }
                }
                if (alphaNumericMatch) {
                    validLicenseId = true;
                    break;
                }

            } else {
                continue;
            }
        }
        return validLicenseId;
    }

    function validate() {
        var filledFieldsCount =
            requiredInputFields.filter(
                function () {
                    return $(this).val().length > 0;
                }).length +
            requiredCheckboxFields.filter(
                function () {
                    return $(this).is(":checked");
                }).length +
            requiredRadioFields.filter(
                function () {
                    return $('input[name=' + $(this).attr("name") + ']:checked').length > 0;
                }).length;

        if (filledFieldsCount == requiredFieldCount) {
            $("form.register :submit").prop("disabled", false);
        } else {
            $("form.register :submit").prop("disabled", true);
        }
    }

    requiredInputFields.bind("change keyup", validate);
    requiredCheckboxFields.bind("change keyup", validate);
    requiredRadioFields.bind("change keyup", validate);
    validate();
    
    var phoneSelector = document.querySelector(".phonenumber");
    if(phoneSelector)
        VMasker(phoneSelector).maskPattern("(999) 999-9999");

    var ssnSelector = document.querySelector(".ssn");
    if(ssnSelector)
        VMasker(ssnSelector).maskPattern("9999");

    var dateSelector = document.querySelector(".date");
    if(dateSelector)
        VMasker(dateSelector).maskPattern("99/99/9999");


    $('[data-toggle="popover"]').popover();

    $('input:not([readonly="readonly"])').not(":hidden").first().focus();
    $('input, textarea').placeholder();

    //$("select#language").on("change", function() {
    //    $("form#language-selector").submit();
    //});
    $("a#language-spanish").on("click", function () {
        $("form#language-selector input#language").val("es");
        $("form#language-selector").submit();
    });
    $("a#language-english").on("click", function () {
        $("form#language-selector input#language").val("en");
        $("form#language-selector").submit();
    });

    //if (window.location.href.indexOf('done') > -1) {
    //    if (window.parent.document.getElementById('organize_registration_btn') !== undefined) {
    //        window.parent.document.getElementById('organize_registration_btn').innerHTML = 'Donate Again?';
    //    }
    //}
    if ($('#license-id-formats').length) {
        var licenseIdFormatsDivContent = $('#license-id-formats').text();
        var jsonLicenseIdFormats = JSON.parse(licenseIdFormatsDivContent);
        $("#proceed").click(function (event) {
            $(".register").submit();
        });
        $(".register").submit({
            jsonLicenseIdFormats: jsonLicenseIdFormats
        }, submitOnLicenseIdValidation);
    }

    function submitOnLicenseIdValidation(event) {
        var licenseIdValue = getLicenseIdField().val();
        var jsonLicenseIdFormats = event.data.jsonLicenseIdFormats;
        var isLicenseIdRequired = checkRequiredLicenseId();
        var isWarningModalShow = $('#warningModal').hasClass('in');
        if (!isLicenseIdNotApplicable(licenseIdValue)) {
            if (isLicenseIdRequired || (licenseIdValue && !isLicenseIdRequired)) {
                var isLicenseIdValid = validateLicenseId(jsonLicenseIdFormats, licenseIdValue);
                if (!(isLicenseIdValid || isWarningModalShow)) {
                    event.preventDefault();
                    $('#warningModal').modal('show');

                    $("#cancel").click(function (event) {
                        $('#warningModal').modal('hide');
                    });

                } else if (!isLicenseIdValid && isWarningModalShow) {
                    $('#warningModal').modal('hide');
                }
            }
        }

    }

    function checkRequiredLicenseId() {
        var licenseIdField = getLicenseIdField();
        return licenseIdField.attr('required') !== undefined ? true : false;
    }

    function getLicenseIdField() {
        var licenseIdField = $("input[id$='license_id']");
        return licenseIdField;
    }

    function isLicenseIdNotApplicable(licenseIdValue) {
        var isNotApplicable = false;
        var notApplicableValues = ["na", "n/a"];
        if (notApplicableValues.indexOf(licenseIdValue.toLowerCase()) >= 0) {
            isNotApplicable = true;
        }
        return isNotApplicable;
    }
});

function showUpennAboutModal() {
    var isAboutModalVisible = $('#upennAboutModal').hasClass('in');
    if (!isAboutModalVisible) {
        $('#upennAboutModal').modal('show');
    }
}
