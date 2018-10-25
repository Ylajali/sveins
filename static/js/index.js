

$(document).ready(function () {



  // SHOW LOGIN FORM
  // SHOW LOGIN FORM
  // SHOW LOGIN FORM
  $("#login-a").click(function() {
    $(".hide-copyright").hide();
    $("#login-form").show();
    window.scrollTo(0,document.body.scrollHeight);
    return false;
  });

  // LEGG TIL SHOW/HIDE
  // LEGG TIL SHOW/HIDE
  // LEGG TIL SHOW/HIDE

  $(".add-items").click(function() {
    $(".cancel-new").trigger("click");
    $(this).parent().find(".add-items-form").toggle();
    $(this).hide();
  })

  $('.cancel-new').click(function () {
    $(".add-items").show();
    $(".add-items-form").hide();
  })

  // SIKKER?
  // SIKKER?
  // SIKKER?
  // SIKKER?
  $(".delete-button").click(function() {
    $( this )
      .parents(".delete-form")
        .find(".yes-no")
          .show();

    $( this ).hide();
    $( this ).parents(".delete-form").find(".usure").css({"display": "inline"});
  });

  // NO DELETE
  // NO DELETE
  // NO DELETE
  $(".no").click(function() {
    var parent =
      $( this )
        .parents(".delete-form");

    parent.find(".delete-button").show();
    parent.find(".yes-no").hide();
    parent.find(".usure").hide();

    return false;
  });




    // REDIGER/LUKK TOGGLE
    // REDIGER/LUKK TOGGLE
    // REDIGER/LUKK TOGGLE
    // REDIGER/LUKK TOGGLE
    $(".show-hide").click(function() {


      // FUNCTION GLOBALS
      var container = $( this ).data('selector');
      var border_bottom = $( this ).data('border');
      var edit_container =
        $( this )
          .parents(container);



          if (border_bottom) {
            // REMOVE BORDER
            var current_border_bottom = edit_container.find(".main-form-group");

            if (current_border_bottom.hasClass("border-bottom")) {
              current_border_bottom.removeClass("border-bottom");
            }
            else {
              current_border_bottom.addClass("border-bottom");
            }
          }

      // CHECKS IF DELETE YES/NO IS ACTIVE
      if ($('.usure').is(":visible")) {
        edit_container.find(".no").trigger("click");
      }

      // TOGGLE REDIGER BUTTON
      if ($( this ).html() === "rediger") {
        $( this ).html("lukk")
      }
      else {
        $( this ).html("rediger")
      }

      // TOGGLE SUBMIT BUTTONS
      edit_container
        .find(".hidden")
          .toggle();

      // TOGGLE INPUTS & TEXTAREA
      var input_selector =
        edit_container
          .find("input, textarea");

      input_selector.toggleClass("input");

      // READONLY TOGGLE
      if (input_selector.prop('readonly')) {
        input_selector.prop('readonly', false);
      }
      else {
        input_selector.prop('readonly', true);
      }



      // NO REFRESH TY
      return false;

    });

    // TRANSITION TRANSITION
    // TRANSITION TRANSITION

    // PREVIOUS LOCATION
    var referrer = document.referrer;
    var find = referrer.split('/');

    // CURRENT LOCATION
    var current_url = window.location.href;
    var find_two = current_url.split("/");

    if (find[3] === "") {
      $('.transition')
      .css({
        bottom: "0%"
      })
      .animate({
        bottom: "150%"
      }, 600);
    }

    // ON CLICK
    // ON CLICK
    $('.nav-home').click(function(e) {
      e.preventDefault();
      var goTo = $(this).attr('href');

      $('.transition').animate({
        bottom: "0%"
      }, 600)

      console.log("hello?")

      setTimeout(function() {
        window.location = goTo;
      }, 600);
    })



    // INDEX INDEX
    // INDEX INDEX
    // INDEX INDEX


    $('.hide-JS-only').fadeIn(1000);

    $('.index-buttons').click(function(e) {
      e.preventDefault();
      var goTo = $(this).attr('onclick');

      $('.index-container, .index-footer').finish().fadeOut(600);

      setTimeout(function() {
        window.location = goTo;
      }, 900);
    })



})
