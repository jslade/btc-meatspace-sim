# Bitcoin Meatspace Simulator

An interactive web application that simulates Bitcoin transactions in physical space (meatspace).

## Features

- **Interactive Canvas**: Visual representation of people and merchants in a physical space
- **Entity Management**: Add people (blue) and merchants (green) to the simulation
- **Bitcoin Transactions**: Simulate Bitcoin transactions between entities
- **Random Walk**: Make entities move around the space randomly
- **Real-time Statistics**: Track the number of people, merchants, transactions, and total BTC
- **Transaction Log**: View a detailed log of all activities and transactions

## How to Use

1. Open `index.html` in a web browser
2. Click "Add Person" to add individuals to the simulation
3. Click "Add Merchant" to add merchant locations
4. Click "Start Transaction" to execute a random Bitcoin transaction
5. Click "Random Walk" to make entities move around
6. Click on entities in the canvas to select them and view their BTC balance
7. Use "Reset" to clear the simulation and start over

## Technologies Used

- HTML5 Canvas for rendering
- Vanilla JavaScript (ES6+)
- CSS3 for styling

## Files

- `index.html` - Main HTML structure
- `app.js` - Simulation logic and canvas rendering
- `style.css` - Styling and layout
- `README.md` - This documentation

## Simulation Details

- Each entity starts with a random amount of BTC (0 to 0.5 BTC)
- Transactions transfer 30% of the sender's balance (max 0.06 BTC per transaction)
- The canvas shows a grid representing physical space
- Entities are visualized with icons (👤 for people, 🏪 for merchants)
- Transaction animations show the flow of BTC between entities

## Running Locally

Simply open the `index.html` file in any modern web browser. No build process or server required!

Alternatively, you can serve it with a local server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js http-server
npx http-server

# Using PHP
php -S localhost:8000
```

Then navigate to `http://localhost:8000` in your browser.
