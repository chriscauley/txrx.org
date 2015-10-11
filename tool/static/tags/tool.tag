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
      <div class="row">
        <div each={ columns } class="col-sm-6">
          <div each={ rows } style="background-color: {this.color}" class="well">
            <a onclick={ parent.parent.loadPermission } each={ permissions } class="permission">
              { abbreviation }
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm-8">
      <permission></permission>
    </div>
  </div>
  <style scoped>
    .permission { cursor: pointer; display: block; color: inherit; font-weight: bold; }
  </style>

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
