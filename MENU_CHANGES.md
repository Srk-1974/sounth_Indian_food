# Menu.jsx Manual Changes for Admin Dashboard

## Change 1: Update Props (Line 7)

**Find this line:**
```javascript
const Menu = ({ items, onAdd, onDelete, onEdit, onAddToCart, user, onLogout, merchantVpa, onUpdateVpa, currency, onUpdateCurrency, darkMode, toggleDarkMode }) => {
```

**Replace with:**
```javascript
const Menu = ({ items, onAdd, onDelete, onEdit, onAddToCart, user, onLogout, merchantVpa, onUpdateVpa, currency, onUpdateCurrency, darkMode, toggleDarkMode, onShowAdminDashboard }) => {
```

---

## Change 2: Add Dashboard Button (Around Line 77-82)

**Find this section:**
```javascript
                <button onClick={() => setShowSettings(true)} className="settings-btn" title="Settings">
                    <FaCog />
                </button>
                <button onClick={onLogout} className="logout-btn">Logout</button>
```

**Replace with:**
```javascript
                <button onClick={() => setShowSettings(true)} className="settings-btn" title="Settings">
                    <FaCog />
                </button>
                {onShowAdminDashboard && (
                    <button 
                        onClick={onShowAdminDashboard} 
                        className="admin-btn" 
                        title="View Login Activity"
                    >
                        📊 Dashboard
                    </button>
                )}
                <button onClick={onLogout} className="logout-btn">Logout</button>
```

---

## That's It!

These are the only two changes needed in Menu.jsx. After making these changes:

1. Save the file
2. The app should compile without errors
3. You'll see a "📊 Dashboard" button in the header
4. Clicking it will show the Admin Dashboard (once Firebase is configured)

---

## Next Steps After This:

1. **Configure Firebase** - Update `src/config/firebase.js` with your Firebase credentials
2. **Add CSS** - Copy the Admin Dashboard styles from the walkthrough.md to `src/index.css`
3. **Test** - Login and click the Dashboard button to see login activity
