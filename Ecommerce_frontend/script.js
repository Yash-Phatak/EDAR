// script.js

document.addEventListener("DOMContentLoaded", () => {
  const productGrid = document.getElementById("product-grid");

  // Mock API response with recommended product IDs
  const apiResponse = {
    recommended_ids: [
      "c2d766ca982eca8304150849735ffef9",
      "7f7036a6d550aaa89d34c77bd39a5e48",
      "f449ec65dcbc041b6ae5e6a32717d01b",
    ],
  };

  // Mock product database
  const productDatabase = {
    c2d766ca982eca8304150849735ffef9: {
      product_name: "Alisha Solid Women's Cycling Shorts",
      retail_price: 999,
      discounted_price: 379,
      images: [
        "http://img5a.flixcart.com/image/short/u/4/a/altht-3p-21-alisha-38-original-imaeh2d5vm5zbtgg.jpeg",
        "http://img5a.flixcart.com/image/short/p/j/z/altght4p-26-alisha-38-original-imaeh2d5kbufss6n.jpeg",
      ],
      brand: "Alisha",
    },
    "7f7036a6d550aaa89d34c77bd39a5e48": {
      product_name: "FabHomeDecor Fabric Double Sofa Bed",
      retail_price: 32157,
      discounted_price: 22646,
      images: [
        "http://img6a.flixcart.com/image/sofa-bed/j/f/y/fhd112-double-foam-fabhomedecor-leatherette-black-leatherette-1100x1100-imaeh3gemjjcg9ta.jpeg",
        "http://img6a.flixcart.com/image/sofa-bed/j/f/y/fhd112-double-foam-fabhomedecor-leatherette-black-leatherette-original-imaeh3gemjjcg9ta.jpeg",
      ],
      brand: "FabHomeDecor",
    },
    f449ec65dcbc041b6ae5e6a32717d01b: {
      product_name: "AW Bellies",
      retail_price: 999,
      discounted_price: 499,
      images: [
        "http://img5a.flixcart.com/image/shoe/7/z/z/red-as-454-aw-11-original-imaeebfwsdf6jdf6.jpeg",
        "http://img6a.flixcart.com/image/shoe/7/z/z/red-as-454-aw-11-original-imaeebfwsdf6jdf6.jpeg",
      ],
      brand: "AW",
    },
  };

  // Function to create and return a product card HTML element
  function createProductCard(product) {
    const productDiv = document.createElement("div");
    productDiv.classList.add("product");

    const productImage = document.createElement("img");
    // productImage.src = product.images[0]; // Display the first image as thumbnail
    console.log(parseMalformedUrlString(product.image));
    productImage.src = parseMalformedUrlString(product.image)[0];
    productImage.alt = product.product_name;

    const productName = document.createElement("h3");
    productName.textContent = product.product_name;

    const productPrice = document.createElement("p");
    productPrice.textContent = `$${product.discounted_price}`;

    const addToCartButton = document.createElement("button");
    addToCartButton.textContent = "Add to Cart";

    productDiv.appendChild(productImage);
    productDiv.appendChild(productName);
    productDiv.appendChild(productPrice);
    productDiv.appendChild(addToCartButton);

    return productDiv;
  }

  // Display products in the grid based on the recommended IDs
  function displayRecommendedProducts(data) {
    data.forEach((product) => {
      if (product) {
        const productCard = createProductCard(product);
        productGrid.appendChild(productCard);
      }
    });
  }

  async function importCSV(filePath) {
    try {
      const response = await fetch(filePath);
      const csvData = await response.text();

      // Parse the CSV data
      const rows = csvData.trim().split("\n");
      const data = rows.map((row) => row.split(","));

      return data;
    } catch (error) {
      console.error("Error importing CSV:", error);
      return [];
    }
  }

  async function getData() {
    const csvData = await fetch("data.json");
    const data = await csvData.json();
    return data;
  }

  var csvData = getData();
  var displayData = [];

  function parseMalformedUrlString(str) {
    // Remove any occurrences of double double-quotes (""), which are causing the issue
    let cleanedStr = str.replace(/""/g, '"');

    // Add closing bracket if it is missing, assuming the string should be a valid array
    if (!cleanedStr.endsWith("]")) {
      cleanedStr += "]";
      //   throw new Error("Malformed JSON: Missing closing bracket");
    }

    // Now parse the corrected string as a JSON array
    try {
      const parsedArray = JSON.parse(cleanedStr);
      return parsedArray;
    } catch (error) {
      throw new Error("Invalid JSON format");
    }
  }

  async function fetchFromServer() {
    const res = await fetch(
      "https://5bcsr2jw-8000.inc1.devtunnels.ms/recommend",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    console.log(res);
    const r = await res.json();
    let resp = [];
    const data = await getData();
    r.recommended_ids.forEach((id) => {
      const item = data.find((item) => item.uniq_id === id);
      resp.push(item);
    });
    console.log(resp);
    displayRecommendedProducts(resp);
  }

  // Call the display function to show recommended products
  getData();
  fetchFromServer();
  //   displayRecommendedProducts();
});
