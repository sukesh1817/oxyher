$(document).ready(function () {

    function checkPasswordStrength(password) {
        var number = /([0-9])/;
        var alphabets = /([a-zA-Z])/;
        var special_characters = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;
        if (password.length < 6) {
           return "should be atleast 6 characters";
        } else {
            if (password.match(number) && password.match(alphabets) && password.match(special_characters)) {
               return "TRUE";
            }
            else {
               return "should include alphabets, numbers and special characters"
            }
        }
    }



    $("#InputEmail").keypress(function () {
        const validateEmail = (email) => {
            return String(email)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                );
        };
        value = $(this).val();
        if (validateEmail(value)) {
            $(this).css("border-color", "#00ba67");
            $("#email-validate-1").show()
            $("#email-validate-0").hide()
        } else {
            $(this).css("border-color", "#ff0015")
            $("#email-validate-1").hide()
            $("#email-validate-0").show()
        }
    });



    $("#InputEmail").blur(function () {
        const validateEmail = (email) => {
            return String(email)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                );
        };
        value = $(this).val();
        if (validateEmail(value)) {
            $(this).css("border-color", "#00ba67");
            $("#email-validate-1").show()
            $("#email-validate-0").hide()
        } else {
            $(this).css("border-color", "#ff0015")

            $("#email-validate-1").hide()
            $("#email-validate-0").show()
        }
    });

   

    // $("#InputEmail").focus(function () {
    //     const validateEmail = (email) => {
    //         return String(email)
    //             .toLowerCase()
    //             .match(
    //                 /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    //             );
    //     };
    //     value = $(this).val();
    //     if (validateEmail(value)) {
    //         $(this).css("border-color", "#00ba67");
    //         $("#email-validate-1").show()
    //         $("#email-validate-0").hide()
    //     } else {
    //         $(this).css("border-color", "#ff0015")

    //         $("#email-validate-1").hide()
    //         $("#email-validate-0").show()
    //     }
    // });








    // $("#InputPassword").focus(function () {
    //     var value = $(this).val();
    //     var result = checkPasswordStrength(value);
    //     if (result == "TRUE") {
    //         console.log("success focus")
    //     } else {
    //         console.error("success focus")

    //     }
    // });

    $("#InputPassword").keypress(function () {
        var value = $(this).val();
        var result = checkPasswordStrength(value);
        if (result == "TRUE" ) {
            $(this).css("border-color", "#00ba67");
            $("#password-validate-1").show()
            $("#password-validate-0").hide()

        } else {
            $(this).css("border-color", "#ff0015")

            $("#password-validate-1").hide()
            $("#password-validate-0").show()

        }
    });
    $("#InputPassword").blur(function () {
        var value = $(this).val();
        var result = checkPasswordStrength(value)
        if ( result == "TRUE") {
            $(this).css("border-color", "#00ba67");
            $("#password-validate-1").show()
            $("#password-validate-0").hide()

        } else {
            $(this).css("border-color", "#ff0015")

            $("#password-validate-1").hide()
            $("#password-validate-0").show()

        }
    });
});