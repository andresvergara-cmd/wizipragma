import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout/Layout'
import Home from './pages/Home'
import Marketplace from './pages/Marketplace'
import ProductDetail from './pages/ProductDetail'
import Transactions from './pages/Transactions'
import { WebSocketProvider } from './context/WebSocketContext'
import { ChatProvider } from './context/ChatContext'
import './App.css'

function App() {
  return (
    <WebSocketProvider>
      <ChatProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/marketplace" element={<Marketplace />} />
              <Route path="/product/:id" element={<ProductDetail />} />
              <Route path="/transactions" element={<Transactions />} />
            </Routes>
          </Layout>
        </Router>
      </ChatProvider>
    </WebSocketProvider>
  )
}

export default App
