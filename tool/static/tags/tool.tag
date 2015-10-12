<tool-checkout>
  <div each={ permissions }>
    <div each={ criteria }>
      { name }
    </div>
  </div>

  this.permissions = window.TXRX.permissions;

</tool-checkout>

<badge>
  <div class="row">
    <div class="col-sm-4">
      <div class="badge-box">
        <div class="row">
          <div each={ opts.columns } class="col-sm-6">
            <div each={ rows } style="background-color: {this.color}" class="{ group: true, any: any }">
              <a onclick={ parent.parent.loadPermission } each={ permissions }
                 class="{ permission: true, has: has, has_not: !has }">
                { abbreviation }
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm-8">
      <permission></permission>
    </div>
  </div>

  var that = this;
  this.on("mount",function() {
    this.user = window.TXRX.user;
    this.opts.columns.forEach(function(i) {
      i.rows.forEach(function(i2) {
        i2.permissions.forEach(function(i3) {
          if (that.user.permission_ids.indexOf(i3.id) > -1) { i3.has = i2.any = true; }
        });
      });
    });
    this.update();
  });
  loadPermission(e) {
    riot.mount("permission",e.item);
  }

</badge>

<permission>
  <h1>{ opts.name }</h1>
  <div each={ opts.criteria_json }>
    <h2>{ name }</h2>
    <div each={ courses }>{ name }</div>
  </div>
  
</permission>

<authorize-criterion>
  <h1>{ opts.name }</h1>
  <input type="text" name="q" onkeyup={ search } placeholder="Search by name or email" />
  
  search(e) {
    uR.bounce(s,[e]);
  }
  function s(e) { console.log(e) }
</authorize-criterion>
