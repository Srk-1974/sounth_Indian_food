import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Menu from './components/Menu';
import Cart from './components/Cart';
import PaymentModal from './components/PaymentModal';
import ChatBot from './components/ChatBot';
import Footer from './components/Footer';
import HeaderBanner from './components/HeaderBanner';

function App() {
  // Load initial data from localStorage or use defaults
  const [user, setUser] = useState(null);
  const [items, setItems] = useState(() => {
    const saved = localStorage.getItem('menuItems');
    return saved ? JSON.parse(saved) : [
      { id: 1, name: 'IDLY', price: 10, image: '/assets/idly.png', category: 'Breakfast' },
      { id: 2, name: 'DOSHA', price: 20, image: '/assets/dosa.png', category: 'Breakfast' },
      { id: 3, name: 'VADA', price: 30, image: '/assets/vada.png', category: 'Snacks' },
      { id: 4, name: 'POORI', price: 40, image: '/assets/poori.png', category: 'Breakfast' },
      { id: 5, name: 'Tea', price: 10, image: '/assets/tea.png', category: 'Beverages' },
      { id: 6, name: 'Coffee', price: 15, image: '/assets/coffee.png', category: 'Beverages' },
    ];
  });
  const [cart, setCart] = useState(() => {
    const saved = localStorage.getItem('cart');
    return saved ? JSON.parse(saved) : [];
  });
  const [showPayment, setShowPayment] = useState(false);
  const [merchantVpa, setMerchantVpa] = useState(() => {
    return localStorage.getItem('merchantVpa') || 'merchant@upi';
  });
  const [currency, setCurrency] = useState(() => {
    const saved = localStorage.getItem('currency');
    return saved ? JSON.parse(saved) : { code: 'INR', symbol: '₹', rate: 1 };
  });

  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });

  const handleUpdateVpa = (newVpa) => {
    setMerchantVpa(newVpa);
  };

  const handleUpdateCurrency = (newCurrency) => {
    setCurrency(newCurrency);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  // Save data to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('menuItems', JSON.stringify(items));
  }, [items]);

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    localStorage.setItem('merchantVpa', merchantVpa);
  }, [merchantVpa]);

  useEffect(() => {
    localStorage.setItem('currency', JSON.stringify(currency));
  }, [currency]);

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  const handleLogin = (username) => {
    setUser(username);
  };

  const handleLogout = () => {
    setUser(null);
    setCart([]);
  };

  const handleAddItem = (item) => {
    const newItem = { ...item, id: Date.now() };
    setItems([...items, newItem]);
  };

  const handleDeleteItem = (id) => {
    setItems(items.filter((item) => item.id !== id));
  };

  const handleEditItem = (updatedItem) => {
    setItems(items.map((item) => (item.id === updatedItem.id ? updatedItem : item)));
  };

  const handleAddToCart = (item) => {
    setCart((prevCart) => {
      const existingItem = prevCart.find((cartItem) => cartItem.id === item.id);
      if (existingItem) {
        return prevCart.map((cartItem) =>
          cartItem.id === item.id
            ? { ...cartItem, quantity: cartItem.quantity + 1 }
            : cartItem
        );
      }
      return [...prevCart, { ...item, quantity: 1 }];
    });
  };

  const handleRemoveFromCart = (id) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== id));
  };

  const handleCheckout = () => {
    setShowPayment(true);
  };

  const handlePaymentSuccess = () => {
    setCart([]);
    setShowPayment(false);
  };

  const cartTotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="app-container">
      {user ? (
        <>
          <div className="main-content">
            <HeaderBanner />
            <Menu
              user={user}
              items={items}
              onAdd={handleAddItem}
              onDelete={handleDeleteItem}
              onEdit={handleEditItem}
              onAddToCart={handleAddToCart}
              onLogout={handleLogout}
              merchantVpa={merchantVpa}
              onUpdateVpa={handleUpdateVpa}
              currency={currency}
              onUpdateCurrency={handleUpdateCurrency}
              darkMode={darkMode}
              toggleDarkMode={toggleDarkMode}
            />
            <Footer />
          </div>
          <Cart
            cartItems={cart}
            onRemove={handleRemoveFromCart}
            onCheckout={handleCheckout}
            currency={currency}
          />
          {showPayment && (
            <PaymentModal
              total={cartTotal}
              onClose={() => setShowPayment(false)}
              onPaymentSuccess={handlePaymentSuccess}
              merchantVpa={merchantVpa}
              currency={currency}
            />
          )}
          <ChatBot
            items={items}
            onAddToCart={handleAddToCart}
            currency={currency}
            cart={cart}
            onRemoveFromCart={handleRemoveFromCart}
            onCheckout={handleCheckout}
          />
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
