import React, { createContext, useContext, useState } from "react";
import { fetchSentimentData } from "../services/api";

const ProductContext = createContext();

export const ProductProvider = ({ children }) => {

  const [productData, setProductData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeProduct = async (productName) => {
    setLoading(true);
    setError(null);

    try {
      const data = await fetchSentimentData(productName);
      setProductData(data);
      setError(null);
      return data;
    } catch (err) {
      setProductData(null);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return (

    <ProductContext.Provider
      value={{
        productData,
        loading,
        error,
        analyzeProduct,
      }}
    >
      {children}
    </ProductContext.Provider>

  );

};

export const useProduct = () => useContext(ProductContext);
