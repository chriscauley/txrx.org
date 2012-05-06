/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.config.forcePasteAsPlainText = true;

CKEDITOR.editorConfig = function( config )
{
  // Define changes to default configuration here. For example:
  config.toolbar_custom_admin = [
    ["Source"],
    ['Maximize', 'ShowBlocks'],
    ['Undo', 'Redo'],
    ['Cut','Copy','Paste','PasteText','PasteFromWord'],
    ['Find', 'Replace'],
    ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
    ['TextColor', 'BGColor'],
    ['SelectAll', 'RemoveFormat'],
      ['Link', 'Unlink', 'Anchor', 'Image'],
    ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
    ['Preview', 'Print'],
    ['SpellChecker', 'Scayt'],
    ['Bold', 'Italic', 'Underline', 'Strike',
     '-', 'Subscript', 'Superscript',
     '-', 'NumberedList', 'BulletedList',
     '-', 'Outdent', 'Indent', 'Blockquote',
     '-', 'Format', 'Font', 'FontSize'],
  ];

  config.toolbar = 'custom_admin';
  config.toolbarCanCollapse = false;
};
