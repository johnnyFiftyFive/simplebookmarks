$(document).on("click", ".open-editLinkDialog", function () {
    var linkId = $(this).data('id');
    var parent = $(this).parent();
    var linkHref = parent.find("#link-" + linkId + "-itm");
    $("#link-title").val(linkHref.text());
    $("#link-address").val(linkHref.attr("href"));
    $("#confirmBtn").val(linkId);
});

$("#confirmBtn").click(function () {

});

$(".delete-link").click(function () {
    var id = $(this).data('id');
    $.post("/delete/" + id);
    $("#link-" + id).remove();
});

