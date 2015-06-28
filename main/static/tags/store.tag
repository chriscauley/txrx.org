<product-list>
  <div class="category" each={ opts.categories }>
    <h1>{ name }</h1>
    <div class="row">
      <product each={ product,i in products } data={ product } class="col-sm-4"></product>
    </div>
  </div>
</product-list>

<product>
  <div class="well {incart:opts.data.quantity}">
    <img src={ opts.data.img.url } />
    <div class="name">{{ opts.data.name }}</div>
    <div class="row">
      <div class="col-sm-6 price">${opts.data.price}</div>
      <div class="col-sm-6">
        <span if={ opts.data.quantity }>x { opts.data.quantity }</span>
        <button class="btn btn-success btn-block" onclick={ plusOne } if={ !opts.data.quantity }>Add to Cart</button>
      </div>
    </div>
    <div if={ opts.data.quantity } class="row">
      <div class="col-sm-6">
        <button class="btn btn-success btn-block" onclick={ plusOne }>+1</button>
      </div>
      <div class="col-sm-6">
        <button class="btn btn-danger btn-block" onclick={ minusOne }>-1</button>
      </div>
      <div class="col-sm-12">
<br />
        <button class="btn btn-primary btn-block" onclick={ minusOne }>Checkout</button>
      </div>
    </div>
  </div>
  opts.data.quantity = 0;
  plusOne(e) {
    opts.data.quantity++;
  }
  minusOne(e) {
    opts.data.quantity--;
  }
</product>
