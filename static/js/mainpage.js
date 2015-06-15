$(".open-editLinkDialog").click(function () {
    var linkId = $(this).data('id');
    var parent = $(this).parent();
    var linkHref = parent.find("#link-" + linkId + "-itm");
    $("#link-title").val(linkHref.text());
    $("#link-address").val(linkHref.attr("href"));
    $("#confirmBtn").val(linkId);
});

$("#confirmBtn").click(function () {
    var data = {
        'id':$(this).val(),
        'title': $("#link-title").val(),
        'url': $("#link-address").val()};
    if(!data['title'] || !data['url']){
        alert("Pola nie moga być puste");
        return;
    }
    $.post("/update/" + data['id'], data);
    $("#linkEditModal").modal('hide');
    window.location.reload();
});

$(".delete-link").click(function () {
    var id = $(this).data('id');
    $(this).parent().slideUp(300, function () {
           $.post("/delete/" + id);
           $("#link-" + id).remove();
    });

});

