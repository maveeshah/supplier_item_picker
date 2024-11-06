## Supplier Item Picker

This custom Frappe app was developed for client in the Philippines to streamline the process of selecting supplier items, generating barcodes for those items, and integrating custom reporting features. The app includes functionalities like supplier-based item selection, barcode generation, and detailed reporting for item deliveries, warehouse stock, and sales invoicing.

---

## Features

### 1. **Supplier Item Selec  tion and Filtering**
- **Multi-supplier Item Picker**: Allows users to select items from a specific supplier or all suppliers, with the ability to filter by item name or item code.
- **Search Functionality**: A built-in search bar in the modal to filter items based on text input, helping users quickly find the desired items from a list.
  
### 2. **Barcode Integration**
- **Dynamic Barcode Generation**: Generates EAN-13 barcodes for selected items. The barcode is saved as an image and can be embedded in the item details.
- **Item Code and Name on Barcode**: The barcode image is customized to include the item's code and name, enhancing visual identification during scanning or inventory management.

### 3. **Custom Reports**
The app includes the following custom reports tailored to the needs of your business:

- **Billed Items to Be Delivered**:
   - Provides a report that lists all billed items which are yet to be delivered, helping the business track pending deliveries.
   
- **Display and Storage Warehouse Stock Summary**:
   - Displays a comprehensive summary of stock levels across various warehouses, including display and storage locations. Useful for inventory control and stock audits.
   
- **Item-wise Sales Invoice with Margin and Discount**:
   - Generates a detailed report of sales invoices broken down by individual item. It includes margin calculations, discounts applied, and other item-level financial details to give a clear picture of profitability.

---

## Installation

To install the Supplier Item Picker app on your Frappe instance, follow these steps:

1. **Clone the Repository**:
   
   Clone the repository to your server using the following command:
   
   ```bash
   git clone https://github.com/[your-username]/[your-app-name].git
   ```

2. **Install the App**:

   Use the following command to install the app:
   
   ```bash
   bench --site [your-site-name] install-app [your-app-name]
   ```

3. **Restart the Bench**:

   Restart the server to make sure everything loads properly:
   
   ```bash
   bench restart
   ```

---

## Configuration

### 1. **Item and Supplier Setup**:
   - Ensure that the **Supplier** and **Item** doctypes are correctly set up with relevant information, including item codes and supplier associations. This is crucial for the `get_items()` and `get_items_details()` methods to work properly.

### 2. **Barcode Field**:
   - Add a **Barcode** field in the `Item Barcode` doctype to store the generated barcode image and link it to each item. The barcode will also be saved as an image file under `public/files/`.

### 3. **Reports Setup**:
   - The following custom reports are already integrated within the app:
     - **Billed Items to Be Delivered**
     - **Display and Storage Warehouse Stock Summary**
     - **Item-wise Sales Invoice with Margin and Discount**

   These reports can be accessed via the Reports section in the Frappe UI.

---

## Usage

### 1. **Fetching Supplier Items in Purchase Order**:
   - In the **Purchase Order** form, a button called **"Get Supplier Items"** will appear (if the form is in a draft state and not a return).
   - Clicking the button will trigger a modal where you can filter and select items from the supplier, which will be added to the purchase order.

### 2. **Generating Barcodes for Items**:
   - Go to the **Item Barcode** form, and you can manually create a barcode for an item by either entering a barcode number or letting the system generate one for you.
   - Once the barcode is created, the barcode image will be displayed, and the barcode number will be stored.

### 3. **Searching and Selecting Items**:
   - The **Item Picker** modal allows searching for items by item name or code. You can select multiple items to add to your form (e.g., Purchase Order).


#### License

mit
