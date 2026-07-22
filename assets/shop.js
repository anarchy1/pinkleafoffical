/* Pink Leaf Shop Logic */
(function(){
  const WHATSAPP = "972559116990";
  let cart = [];

  /* DOM refs */
  const grid = document.getElementById("productGrid");
  const searchInput = document.getElementById("searchInput");
  const sortSelect = document.getElementById("sortSelect");
  const resultsCount = document.getElementById("resultsCount");
  const cartBtn = document.getElementById("cartBtn");
  const cartCount = document.getElementById("cartCount");
  const cartDrawer = document.getElementById("cartDrawer");
  const cartOverlay = document.getElementById("cartOverlay");
  const closeCart = document.getElementById("closeCart");
  const cartItems = document.getElementById("cartItems");
  const cartFooter = document.getElementById("cartFooter");
  const cartTotal = document.getElementById("cartTotal");
  const checkoutBtn = document.getElementById("checkoutBtn");
  const filterBtns = document.querySelectorAll(".filter-btn");

  let activeCategory = "all";

  /* Placeholder SVG for plants without images */
  const placeholderSVG = `<svg class="placeholder-icon" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#c2185b" stroke-width="1.2"><path d="M12 22c-4-3-8-6-8-10a8 8 0 0116 0c0 4-4 7-8 10z"/><path d="M12 12V2"/><path d="M8 6c2 1 4 1 4 1s2 0 4-1"/></svg>`;

  /* Render products */
  function renderProducts(){
    const q = searchInput.value.toLowerCase().trim();
    const sort = sortSelect.value;
    let items = PRODUCTS.filter(function(p){
      if(activeCategory !== "all" && p.category !== activeCategory) return false;
      if(q && !p.name.toLowerCase().includes(q) && !p.category.toLowerCase().includes(q)) return false;
      return true;
    });

    /* Sort */
    items.sort(function(a,b){
      if(sort === "price-asc") return a.price - b.price;
      if(sort === "price-desc") return b.price - a.price;
      if(sort === "name-desc") return b.name.localeCompare(a.name);
      return a.name.localeCompare(b.name);
    });

    resultsCount.textContent = items.length + " צמחים";

    if(!items.length){
      grid.innerHTML = '<div class="no-results"><p>לא נמצאו צמחים</p><p style="font-size:14px">נסו חיפוש אחר</p></div>';
      return;
    }

    grid.innerHTML = items.map(function(p){
      var inCart = cart.find(function(c){ return c.id === p.id; });
      var imgHTML = p.image
        ? '<img src="' + p.image + '" alt="' + p.name + '" loading="lazy">'
        : placeholderSVG;
      return '<div class="product-card">' +
        '<div class="product-img-wrap">' + imgHTML +
          '<span class="product-category-tag">' + p.category + '</span>' +
        '</div>' +
        '<div class="product-info">' +
          '<div class="product-name">' + p.name + '</div>' +
          '<div class="product-category-label">' + p.category + '</div>' +
          '<div class="product-bottom">' +
            '<span class="product-price">₪' + p.price.toLocaleString() + '</span>' +
            '<button class="add-to-cart' + (inCart ? ' added' : '') + '" data-id="' + p.id + '">' +
              (inCart ? '✓ בעגלה' : 'הוסף לעגלה') +
            '</button>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join("");
  }

  /* Cart functions */
  function addToCart(id){
    var product = PRODUCTS.find(function(p){ return p.id === id; });
    if(!product) return;
    var existing = cart.find(function(c){ return c.id === id; });
    if(existing){
      existing.qty++;
    } else {
      cart.push({ id: product.id, name: product.name, price: product.price, image: product.image, qty: 1 });
    }
    updateCartUI();
    renderProducts();
  }

  function removeFromCart(id){
    cart = cart.filter(function(c){ return c.id !== id; });
    updateCartUI();
    renderProducts();
  }

  function changeQty(id, delta){
    var item = cart.find(function(c){ return c.id === id; });
    if(!item) return;
    item.qty += delta;
    if(item.qty <= 0) return removeFromCart(id);
    updateCartUI();
  }

  function updateCartUI(){
    var totalItems = cart.reduce(function(s,c){ return s + c.qty; }, 0);
    var totalPrice = cart.reduce(function(s,c){ return s + c.price * c.qty; }, 0);

    cartCount.textContent = totalItems;
    cartCount.classList.toggle("visible", totalItems > 0);

    if(!cart.length){
      cartItems.innerHTML = '<p class="cart-empty">העגלה ריקה</p>';
      cartFooter.style.display = "none";
    } else {
      cartItems.innerHTML = cart.map(function(c){
        return '<div class="cart-item">' +
          '<div class="cart-item-img" style="display:flex;align-items:center;justify-content:center;font-size:24px">🌿</div>' +
          '<div class="cart-item-details">' +
            '<div class="cart-item-name">' + c.name + '</div>' +
            '<div class="cart-item-price">₪' + (c.price * c.qty).toLocaleString() + '</div>' +
          '</div>' +
          '<div class="cart-item-qty">' +
            '<button class="qty-btn" data-id="' + c.id + '" data-delta="-1">-</button>' +
            '<span>' + c.qty + '</span>' +
            '<button class="qty-btn" data-id="' + c.id + '" data-delta="1">+</button>' +
          '</div>' +
        '</div>';
      }).join("");
      cartFooter.style.display = "block";
      cartTotal.textContent = "₪" + totalPrice.toLocaleString();

      /* Build WhatsApp message */
      var msg = "שלום! אשמח להזמין מ-Pink Leaf:\n\n";
      cart.forEach(function(c){
        msg += c.name + " x" + c.qty + " - ₪" + (c.price * c.qty).toLocaleString() + "\n";
      });
      msg += "\nסה\"כ: ₪" + totalPrice.toLocaleString();
      checkoutBtn.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(msg);
    }
  }

  function openCart(){ cartDrawer.classList.add("open"); cartOverlay.classList.add("open"); }
  function closeCartFn(){ cartDrawer.classList.remove("open"); cartOverlay.classList.remove("open"); }

  /* Event listeners */
  cartBtn.addEventListener("click", openCart);
  closeCart.addEventListener("click", closeCartFn);
  cartOverlay.addEventListener("click", closeCartFn);

  grid.addEventListener("click", function(e){
    var btn = e.target.closest(".add-to-cart");
    if(btn) addToCart(btn.dataset.id);
  });

  cartItems.addEventListener("click", function(e){
    var btn = e.target.closest(".qty-btn");
    if(btn) changeQty(btn.dataset.id, parseInt(btn.dataset.delta));
  });

  filterBtns.forEach(function(btn){
    btn.addEventListener("click", function(){
      filterBtns.forEach(function(b){ b.classList.remove("active"); });
      btn.classList.add("active");
      activeCategory = btn.dataset.category;
      renderProducts();
    });
  });

  searchInput.addEventListener("input", renderProducts);
  sortSelect.addEventListener("change", renderProducts);

  /* Init */
  renderProducts();
})();
