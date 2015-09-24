<flag-list>
  <div class="flag-group" each={ opts.flagsets }>
    <h4 class="italic-title">{ verbose }</h4>
    <div style="width: 400px;">
      <table style="width: 100%;" class="table striped table-striped">
        <tr each={ flags }>
          <td><a href="/admin/membership/userflag/{ pk }/">
              { username } - { product_name }
              <br/>{ reason_display } [{ datetime|date:"m/d/Y" }]
          </a></td>
          <td>
            <button onclick={ ajaxPost } data-action="send"><i class="icon-envelope"></i></button>
            <button onclick={ ajaxPost } data-action="delete"><i class="icon-trash"></i></button>
          </td>
        </tr>
        <tr if={ flags.length == 0 }><td>No Flags, hurray!</td></tr>
      </table>
    </div>
  </div>

  ajaxPost(e) {
    var pk = element.dataset.pk;
    console.log(pk);
  }
  deleteFlag(element) {
    var url = "/flags/delete/";
    ajaxPost(element,url);
  }
</flag-list>
