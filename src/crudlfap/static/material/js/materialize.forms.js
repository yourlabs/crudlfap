window.DjangoMaterial = {
  initForms: function ($container) {
    // Formsets
    // https://bitbucket.org/ionata/django-formset-js
    $('.formset-field').formset({
      animateForms: true,
      newFormCallback: DjangoMaterial.initForms
    })

    // Select
    // http://materializecss.com/forms.html#select
    $container
      .find('select')
      .not('.disabled')
      .not('.material-ignore')
      .material_select()

    var lang = jQuery( ":root" ).attr('lang')
    if(lang) {
      jQuery.datetimepicker.setLocale(lang.substr(0, 2));
    }

    // Date/DateTime/Time
    // https://github.com/xdan/datetimepicker
    $container
      .find('[data-form-control="date"]')
      .each(function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          timepicker: false,
          mask: false,
          scrollInput: false
        })
      })
    $container
      .find('[data-form-control="time"]')
      .each(function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          datepicker: false,
          timepicker: true,
          mask: false,
          scrollInput: false
        })
      })
    $container.find('[data-form-control="datetime"]').each(
      function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          datepicker: true,
          timepicker: true,
          mask: false,
          scrollInput: false
        })
      })
  },

  destroyForms: function ($container) {
    // Select
    $container
      .find('select')
      .not('.disabled')
      .not('.material-ignore')
      .material_select('destroy')

    // Date/DateTime/Time
    $container
      .find('[data-form-control="date"],[data-form-control="time"],[data-form-control="datetime"]')
      .datetimepicker('destroy');
  }
};

(function() {
  if(window.Turbolinks) {
    $(document).on('turbolinks:load', function() { DjangoMaterial.initForms($(document)) })
    $(document).on('turbolinks:before-cache', function () { DjangoMaterial.destroyForms($(document))})
  } else {
    $(document).ready(function() { DjangoMaterial.initForms($(document)) })
  }
})()
