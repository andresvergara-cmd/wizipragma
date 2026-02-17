// Mock Products Data for CENTLI Marketplace
export const mockProducts = [
  {
    id: 'prod-001',
    name: 'MacBook Pro 14" M3',
    description: 'Laptop profesional con chip M3, 16GB RAM, 512GB SSD. Perfecta para trabajo y creatividad.',
    price: 45999,
    originalPrice: 52999,
    category: 'Tecnología',
    subcategory: 'Laptops',
    brand: 'Apple',
    image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800',
    rating: 4.8,
    reviews: 342,
    stock: 15,
    benefits: [
      {
        type: 'CASHBACK',
        value: 5,
        description: '5% de cashback',
        amount: 2300
      },
      {
        type: 'MSI',
        months: [3, 6, 12],
        description: 'Hasta 12 meses sin intereses',
        monthlyPayment: 3833
      }
    ],
    features: [
      'Chip M3 de 8 núcleos',
      '16GB de memoria unificada',
      '512GB de almacenamiento SSD',
      'Pantalla Liquid Retina XDR de 14.2"',
      'Batería de hasta 17 horas'
    ],
    seller: {
      name: 'Apple Store Oficial',
      rating: 4.9,
      verified: true
    }
  },
  {
    id: 'prod-002',
    name: 'iPhone 15 Pro 256GB',
    description: 'El iPhone más avanzado con chip A17 Pro, cámara de 48MP y titanio.',
    price: 28999,
    originalPrice: 32999,
    category: 'Tecnología',
    subcategory: 'Smartphones',
    brand: 'Apple',
    image: 'https://images.unsplash.com/photo-1592286927505-c0d6c9c24e5a?w=800',
    rating: 4.9,
    reviews: 856,
    stock: 28,
    benefits: [
      {
        type: 'CASHBACK',
        value: 8,
        description: '8% de cashback',
        amount: 2320
      },
      {
        type: 'MSI',
        months: [3, 6, 9, 12],
        description: 'Hasta 12 meses sin intereses',
        monthlyPayment: 2417
      },
      {
        type: 'DISCOUNT',
        value: 12,
        description: '12% de descuento',
        amount: 4000
      }
    ],
    features: [
      'Chip A17 Pro',
      'Cámara principal de 48MP',
      'Diseño de titanio',
      'Dynamic Island',
      'USB-C'
    ],
    seller: {
      name: 'Apple Store Oficial',
      rating: 4.9,
      verified: true
    }
  },
  {
    id: 'prod-003',
    name: 'Samsung Galaxy S24 Ultra',
    description: 'Smartphone premium con S Pen, cámara de 200MP y pantalla AMOLED 2X.',
    price: 26999,
    originalPrice: 29999,
    category: 'Tecnología',
    subcategory: 'Smartphones',
    brand: 'Samsung',
    image: 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800',
    rating: 4.7,
    reviews: 523,
    stock: 42,
    benefits: [
      {
        type: 'CASHBACK',
        value: 10,
        description: '10% de cashback',
        amount: 2700
      },
      {
        type: 'MSI',
        months: [6, 12, 18],
        description: 'Hasta 18 meses sin intereses',
        monthlyPayment: 1500
      }
    ],
    features: [
      'Cámara de 200MP',
      'S Pen incluido',
      'Pantalla AMOLED 2X de 6.8"',
      'Snapdragon 8 Gen 3',
      'Batería de 5000mAh'
    ],
    seller: {
      name: 'Samsung Official Store',
      rating: 4.8,
      verified: true
    }
  },
  {
    id: 'prod-004',
    name: 'Sony WH-1000XM5',
    description: 'Audífonos premium con cancelación de ruido líder en la industria.',
    price: 7999,
    originalPrice: 9999,
    category: 'Tecnología',
    subcategory: 'Audio',
    brand: 'Sony',
    image: 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800',
    rating: 4.9,
    reviews: 1245,
    stock: 67,
    benefits: [
      {
        type: 'CASHBACK',
        value: 15,
        description: '15% de cashback',
        amount: 1200
      },
      {
        type: 'MSI',
        months: [3, 6],
        description: 'Hasta 6 meses sin intereses',
        monthlyPayment: 1333
      }
    ],
    features: [
      'Cancelación de ruido adaptativa',
      'Hasta 30 horas de batería',
      'Audio de alta resolución',
      'Multipoint connection',
      'Controles táctiles'
    ],
    seller: {
      name: 'Sony Store',
      rating: 4.7,
      verified: true
    }
  },
  {
    id: 'prod-005',
    name: 'iPad Air M2 11"',
    description: 'Tablet potente y versátil con chip M2 y Apple Pencil Pro compatible.',
    price: 15999,
    originalPrice: 18999,
    category: 'Tecnología',
    subcategory: 'Tablets',
    brand: 'Apple',
    image: 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800',
    rating: 4.8,
    reviews: 432,
    stock: 34,
    benefits: [
      {
        type: 'CASHBACK',
        value: 7,
        description: '7% de cashback',
        amount: 1120
      },
      {
        type: 'MSI',
        months: [3, 6, 9, 12],
        description: 'Hasta 12 meses sin intereses',
        monthlyPayment: 1333
      }
    ],
    features: [
      'Chip M2',
      'Pantalla Liquid Retina de 11"',
      'Compatible con Apple Pencil Pro',
      'Touch ID',
      'USB-C'
    ],
    seller: {
      name: 'Apple Store Oficial',
      rating: 4.9,
      verified: true
    }
  },
  {
    id: 'prod-006',
    name: 'Dell XPS 15',
    description: 'Laptop premium con pantalla OLED 4K y procesador Intel Core i7.',
    price: 38999,
    originalPrice: 44999,
    category: 'Tecnología',
    subcategory: 'Laptops',
    brand: 'Dell',
    image: 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800',
    rating: 4.6,
    reviews: 287,
    stock: 19,
    benefits: [
      {
        type: 'CASHBACK',
        value: 6,
        description: '6% de cashback',
        amount: 2340
      },
      {
        type: 'MSI',
        months: [6, 12],
        description: 'Hasta 12 meses sin intereses',
        monthlyPayment: 3250
      }
    ],
    features: [
      'Intel Core i7 13th Gen',
      'Pantalla OLED 4K de 15.6"',
      '16GB RAM DDR5',
      '512GB SSD NVMe',
      'NVIDIA GeForce RTX 4050'
    ],
    seller: {
      name: 'Dell Official Store',
      rating: 4.7,
      verified: true
    }
  },
  {
    id: 'prod-007',
    name: 'Nintendo Switch OLED',
    description: 'Consola híbrida con pantalla OLED de 7 pulgadas y 64GB de almacenamiento.',
    price: 8499,
    originalPrice: 9999,
    category: 'Gaming',
    subcategory: 'Consolas',
    brand: 'Nintendo',
    image: 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=800',
    rating: 4.9,
    reviews: 1876,
    stock: 89,
    benefits: [
      {
        type: 'CASHBACK',
        value: 10,
        description: '10% de cashback',
        amount: 850
      },
      {
        type: 'MSI',
        months: [3, 6, 9],
        description: 'Hasta 9 meses sin intereses',
        monthlyPayment: 944
      }
    ],
    features: [
      'Pantalla OLED de 7"',
      '64GB de almacenamiento',
      'Dock con puerto LAN',
      'Modo portátil y TV',
      'Joy-Con incluidos'
    ],
    seller: {
      name: 'Nintendo Store',
      rating: 4.9,
      verified: true
    }
  },
  {
    id: 'prod-008',
    name: 'LG OLED C3 55"',
    description: 'Smart TV OLED 4K con procesador α9 Gen6 AI y Dolby Vision.',
    price: 32999,
    originalPrice: 39999,
    category: 'Hogar',
    subcategory: 'Televisores',
    brand: 'LG',
    image: 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800',
    rating: 4.8,
    reviews: 654,
    stock: 23,
    benefits: [
      {
        type: 'CASHBACK',
        value: 8,
        description: '8% de cashback',
        amount: 2640
      },
      {
        type: 'MSI',
        months: [12, 18, 24],
        description: 'Hasta 24 meses sin intereses',
        monthlyPayment: 1375
      }
    ],
    features: [
      'Panel OLED 4K',
      'Procesador α9 Gen6 AI',
      'Dolby Vision IQ',
      'HDMI 2.1 para gaming',
      'webOS 23'
    ],
    seller: {
      name: 'LG Electronics',
      rating: 4.8,
      verified: true
    }
  }
];

export const categories = [
  {
    id: 'tech',
    name: 'Tecnología',
    icon: '💻',
    subcategories: ['Laptops', 'Smartphones', 'Tablets', 'Audio', 'Accesorios']
  },
  {
    id: 'gaming',
    name: 'Gaming',
    icon: '🎮',
    subcategories: ['Consolas', 'Juegos', 'Accesorios', 'PC Gaming']
  },
  {
    id: 'home',
    name: 'Hogar',
    icon: '🏠',
    subcategories: ['Televisores', 'Electrodomésticos', 'Muebles', 'Decoración']
  },
  {
    id: 'fashion',
    name: 'Moda',
    icon: '👔',
    subcategories: ['Ropa', 'Calzado', 'Accesorios', 'Relojes']
  }
];

export const benefitTypes = {
  CASHBACK: {
    name: 'Cashback',
    icon: '💰',
    color: '#4caf50'
  },
  MSI: {
    name: 'Meses sin intereses',
    icon: '📅',
    color: '#2196f3'
  },
  DISCOUNT: {
    name: 'Descuento',
    icon: '🏷️',
    color: '#ff9800'
  },
  POINTS: {
    name: 'Puntos',
    icon: '⭐',
    color: '#9c27b0'
  }
};
