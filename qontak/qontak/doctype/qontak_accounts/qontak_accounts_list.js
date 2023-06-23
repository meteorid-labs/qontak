// Copyright (c) 2023, Meteor Inovasi Digital and contributors
// For license information, please see license.txt

frappe.listview_settings['Qontak Accounts'] = {
  hide_name_column: true,
  add_fields: ['default'],
  get_indicator: function (doc) {
    var colors = {
      1: 'blue',
      0: 'gray'
    }

    var labels = {
      1: 'Default',
      0: 'Not Default'
    }

    return [
      __(labels[parseInt(doc.default)]),
      colors[parseInt(doc.default)],
      'status,=,' + doc.default
    ]
  }
}
