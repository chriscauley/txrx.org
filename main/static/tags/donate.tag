uR.ready(function() { riot.mount("money-widget") });

<money-widget>
  <div class="well">
    <div class="btn-group first">
      <div each={ number in numbers } class="btn btn-{ number == parent.selected_value?'primary':'default' }">
        <input value="{ number }" type="radio" id="money_button_{ number }" onchange={ setIt } name="money_button"/>
        <label for="money_button_{ number }">${ number }</label>
      </div>
      <div class="btn btn-{ other?'primary':'default' }">
        <input type="text" min="1" step="1" onkeyUp={ setOther } onfocus={ setOther } onblur={ setother }
               id="money_other" />
        <label for="money_other">Other</label>
      </div>
    </div>

    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" style="display: none;" id="donation-form">
      <input type="hidden" name="cmd" value="_donations">

      <input type="hidden" name="business" value="txrxlabs@gmail.com">
      <input type="hidden" name="a3" value="{ selected_value }"><!-- price -->
      <input type="hidden" name="p3" value="1"><!-- term delay (# months between payments -->
      <input type="hidden" name="t3" value="M"><!-- term units (months) -->
      <input type="hidden" name="src" value="1"><!-- recurring payments = 1 -->
      <input type="hidden" name="sra" value="1">
      <input type="hidden" name="amount" value="{ selected_value }">
      <input name="notify_url" type="hidden" value="https://txrxlabs.org/tx/rx/ipn/handler/">
      <input name="cancel_return" type="hidden" value="https://txrxlabs.org/support/">
      <input name="return" type="hidden" value="https://txrxlabs.org/">

      <input type="hidden" name="custom" value={ opts.description || 'support page donation' }>

      <input name="on0" type="hidden" value="Donation"/>
      <input name="os0" type="hidden" value="Monthly"/>
      <input type="hidden" name="currency_code" value="USD">
    </form>

    <div class="btn-group second">
      <button onclick={ pay } data-cmd="_donations" class="btn btn-primary">
        { opts.donate_text || "One-time gift" }</button>
      <button onclick={ pay } data-cmd="_xclick-subscriptions" class="btn btn-primary"
              if={ !opts.hide_monthly }>Monthly gift</button>
    </div>
    <div if={ error } class="alert alert-danger">Please select an amount</div>
  </div>
              

  this.numbers = [25,50,150,500];
  setIt(e) {
    this.error = false;
    this.other = false;
    this.selected_value = e.item.number;
  };
  setOther(e) {
    this.error = false;
    this.other = true;
    this.selected_value = e.target.value.replace(/[^\d]+/g,'');
    if (this.root.querySelector(":checked")) { this.root.querySelector(":checked").checked = false; }
  }
  pay(e) {
    if (!this.selected_value) { this.error = true; return; }
    var f = document.querySelector("#donation-form");
    f.querySelector("[name=cmd]").value=e.target.dataset.cmd;
    f.submit();
  }
</money-widget>
