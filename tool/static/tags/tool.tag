<tool-checkout>
  <div each={ permissions }>
    <div each={ criteria }>
      { name }
    </div>
  </div>

  this.permissions = window.TXRX.permissions;
  console.log(this.permissions)

</tool-checkout>
