import { useState } from 'react'
import { Link } from 'react-router-dom'
import './Home.css'

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [currentLocation, setCurrentLocation] = useState(0)

  const locations = [
    {
      title: 'Bibliotecas Comfama',
      description: 'Inspírate con nuestra red de programación literaria y prepárate para viajar por grandes colecciones de libros y revistas.',
      image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAF2RN3RO_vYuvK4EuM2-iUWZwDiWMkH4Vddz9BwFGjyafV6gVnlFR0KgmpQjLDXITMl59IaZzp91Mt2a-Erzlz5l047Nm5rnspNAyi5wH3WWQgHYLfG3qsntWdpyM2Exb6sCSn4p1xELMg4NgmQ61KrP2T8nKKbGmebGTXJkP-4g1bx2hm9iibtjmv59Zm83jeNMiBck3cMuMo71uKVsChUgX1wS07t0RQf9rlN3Txmc_Ulfu2pC0SQ7B4YwgULeRCC_H4iwG-Wcvk'
    },
    {
      title: 'Cosmo School',
      description: 'Te presentamos nuestra red de colegios y su modelo de aprendizaje autónomo, basado en proyectos y experiencias.',
      image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAKvuKMgQT4yCHE-sKfOQThiql_b8VrFpvGi5buGFDORLVvsoDLTe7rHkv_XCbtx_660CyWpsM-EK6F0ydjAXHRadFcUiDZ4Y7K4gU-oIL52hiG2YInrAUxde1e0gng7oduaKgdrPzSa6a4WUg4FOZZd0N-87kJcNvSdLyoKA3qW2rZwWfzUDvbtAHqF51NT41nBvVLKabPyLNoXJWDZqHS-kHvqLWygQtmcLKWa86xpnjM_qMglpOzCcXoVym91Ia1vI3o1y9NmLa5'
    },
    {
      title: 'Claustro Comfama',
      description: 'El arte, la cultura y los saberes conviven en este sitio patrimonial ubicado en el corazón de Medellín.',
      image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCNvwSJ8hMKwdWCBl6Dn88noaYHedaex0hSCJ7SvCHKzOXNpzxosTetLiv84ZxtkkKE6W3FNMalMopTENVRqL07wEVHTyA_WLILzhPMef3zFFq1GY9NUyfzeaklzXJhUw2hxwB_l7U7xavkCgIoLhcZ0VLAXjlJkeLBX_LjaP9SnkwnBeUY7BnbO9xceiWDWNlAQdnzRlYl-sRLyC96BSnhq5wObuOzZdkq0zIa8W5M-nDWTaT0kfFqd-vCyxy6hgyHKQIz0pgrXmax'
    },
    {
      title: 'Parques Comfama',
      description: 'Territorios pensados para tu diversión, encuentro, movimiento y conexión con la naturaleza.',
      image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBIQ0E0beQWrWwJ0UgdfBA49Bk5yccaH0PHmxq61d1mStOguHI3S8pmD_i151G6pk67Us_ZthO_ME7mQuzwn78Vwlk3AW5Audy-NXRlaHU4ybGCSvNMkFmXJZ6QgcstY8EHv_IExsQnkXc9NaCkTtbwedeLbATUx7bKjM9sU687tmk7RzZVw1LV6m8uugNn_nWDUe85gpvTOlUK5hpXQoqbHTX4i0fDUobpsbhxTBQto4_yx-89cAmXPK6lWNcwC11oga3smWUeQ58n'
    },
    {
      title: 'Centros Integrales de Salud',
      description: 'Encuentra el CIS Comfama más cerca de ti, conoce las cuotas moderadoras y gestiona tus citas médicas.',
      image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDU3j6OC8Ejsq9okNKXrYFmsd0OOuBo6cJkXvbsLxqHh0H0N_78UIEPYoiqWdVG9xRKg_xhuYx1pDTGtY8ibO905kSf9IiwMHC66LHQQ2IbUu9VVIDs4S5HiV2ZWnC-p1YB_MO4tEBMTRhWXzdCC8N4Tm1ZmOx2IGPYXRRb8tlZyLWMWgboqDRzV3OttO3Hw4EDqSq24HHFRBaKVWAU_nPByEe7mDWABCwWNYT05HiN2x7Zqbj_yHa04h43gP1TdQAvx_z0ktgRBp0k'
    }
  ]

  const scrollLocations = (direction) => {
    if (direction === 'next') {
      setCurrentLocation((prev) => (prev + 1) % locations.length)
    } else {
      setCurrentLocation((prev) => (prev - 1 + locations.length) % locations.length)
    }
  }

  return (
    <div className="home-comfama">
      {/* Hero Banner */}
      <section className="hero-banner-comfama">
        <div className="hero-content-comfama">
          <span className="hero-tag">FESTIVALES</span>
          <h1>Festival de Animación Comfama</h1>
          <p>Del 12 al 15 de marzo, El Retiro será el escenario para cuidar la vida en todas sus formas a través de la animación.</p>
          <Link to="/marketplace" className="hero-btn">Conoce más aquí</Link>
        </div>
        <div className="hero-image-comfama">
          <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuATIoFfQR86uB6gUdw8BebNjBQBN887_PhW7M5wjUdAytkckB-M6lqVajQJrCGSZx3DBEXjp6iYWuXdR6jHBovEtzotaordHK4xRoxaOPlwBenLmoYrccm4dDiAdB3pvjLQI0_dsAqi-yf9ulZRl4M7q9_8mkWRPuS1LFg8CsSLy7LQxTrSwpYXxb9vUKzz88-mLeh_AEHZLCoHOcayUpEJ5s2QQ1Zi2HXMk1nCEsJJhR30FmPySMOaBIpTkFiSG5mA6BvupyqUoNf_" alt="Hero" />
        </div>
        <div className="hero-dots">
          <span className="dot active"></span>
          <span className="dot"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>
      </section>

      {/* Search Section */}
      <section className="search-section">
        <div className="container-comfama">
          <div className="tab-selector">
            <button className="tab-btn active">Personas y familias</button>
            <button className="tab-btn">Empresas</button>
          </div>
          <h2 className="section-title-brand">¿Qué estás buscando?</h2>
          <p className="section-subtitle">Encuentra en nuestro portafolio distintos programas, servicios y oportunidades que te conectan con el progreso, cuidado y disfrute.</p>
          
          <div className="search-grid">
            <Link to="/marketplace" className="search-card">
              <div className="search-icon">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span>Solicitar crédito</span>
            </Link>
            
            <Link to="/marketplace" className="search-card">
              <div className="search-icon">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <span>Conoce tu tarifa de afiliación</span>
            </Link>
            
            <Link to="/marketplace" className="search-card">
              <div className="search-icon">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span>Viajar</span>
            </Link>
            
            <Link to="/marketplace" className="search-card">
              <div className="search-icon">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                </svg>
              </div>
              <span>Acceder a subsidio de vivienda</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="benefits-section">
        <div className="container-comfama">
          <div className="section-header">
            <span className="section-tag">Descubre un mundo de posibilidades para ti y tu familia.</span>
            <h2 className="section-title-dark">Beneficios Comfama</h2>
          </div>
          
          <div className="benefits-grid">
            <div className="benefit-card">
              <div className="benefit-image">
                <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuCMSNqxknIStcTXufCRalV5hMpEn1QMNqzbfXCMm4DVrq9422jUFc1PFgx0cKpaoC9JK9GCNdaz-E20KbtiaFoj4t4fhoDVIQlEOO_B7w9aACEyRyf3YaHDIAqtY0k9vCv4JSWfeUw2uk5ppbJIUfJ5rud3olAsOAbR8qPvfvJ1pq4qcYP5D6jWg_9E-HJJ3nDbEM7tLsKCYm941Il32hFWKdrwx3ei_FvqvcXNmL5uxfXUidgYlo1QL0Vhun6W-jHa0vIXSitfiNmm" alt="Niños" />
              </div>
              <div className="benefit-content">
                <span className="benefit-tag">Descubre un mundo de posibilidades para</span>
                <h3>Niños</h3>
                <p>Espacios para aprender, crear y jugar, con actividades que fortalezcan la creatividad, los talentos y el desarrollo integral desde los primeros años.</p>
                <button className="benefit-btn">Conocer más</button>
              </div>
            </div>

            <div className="benefit-card">
              <div className="benefit-image">
                <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuAY66dPjOcJqKaa3VKlMLO40vxvS7X-6YFx2ZGEqu361NOXKybKRBeP0o3HMb-hcpmCJQwNiVkn3dCWBUtDFx_rGR3hCKlxoO4lG4OxdOQjlz3wsXdsKUvenx3q2KT5wiFw3kigTdOSajHp_CoO4YK_X3pZZQCTaxihO6RqOmdy7NlWqYDkgzT3jjNoiZoctarkkmyCQih0xxVkYVyhdX4T50N8MvvLde2RqVOEd6KxtuxVwT-UXgym8UUWb02N02bpewOruD0wRjd3" alt="Jóvenes" />
              </div>
              <div className="benefit-content">
                <span className="benefit-tag">Descubre un mundo de posibilidades para</span>
                <h3>Jóvenes</h3>
                <p>Oportunidades para crecer, disfrutar, aprender y construir tu futuro con cursos, programas de formación y espacios de bienestar que te acompañen en cada paso.</p>
                <button className="benefit-btn">Conocer más</button>
              </div>
            </div>

            <div className="benefit-card">
              <div className="benefit-image">
                <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuAYpGDR8JAHPFcAbUazgK1Z9Kere9JjvcdGrMo0oOtxw2_zs0WIwtbLcjf5GdjY58Ec9fxtnu8MmE7u5Jtm78GQ2J32f29g-RmiQdEa7AwX2FtgNKiGEK6PM9enbfR2-GB-Y0wzhiMRFCX7nR6nmG-RDOoL5F0CykqmcQ-zRg8V1iYtPYbrLSJ2KEtq701-Lhkd0UIWZGvk9Q16d6nC8LuK3m7-aNKHoe3oXyVlUfIaiTwgKAO5LvkyMK-AXNB0xqGwhdKzsLw8rM9V" alt="Adultos" />
              </div>
              <div className="benefit-content">
                <span className="benefit-tag">Descubre un mundo de posibilidades para</span>
                <h3>Adultos</h3>
                <p>Espacios para fortalecer tu bienestar, aprender nuevas habilidades y disfrutar experiencias que impulsen tu proyecto de vida en cada etapa.</p>
                <button className="benefit-btn">Conocer más</button>
              </div>
            </div>

            <div className="benefit-card">
              <div className="benefit-image">
                <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuCw6sIQL-yCTG5nzlcyz0oHKodKv5v7w1LggJqYgqqdCIPwkmCfMD9lnUKvx4bHZPsDh7m-7LFQAKYMQIXGQAuz9QsHTPXsrSzrumZ-C1dLyaZdnLXkGlbiYK0W7Xt7AOqcE5oG5tKGiSeQ7d-oPhYIE6qdSKizVy0FecN0QKfMKker5C65lig56aEfurE5nyaX1g9ehxHVcG1NubH-Koofeqw4ndSq0qtnvCLaJr56b0y-WNmKq6UDgMpTrNOe1nbgnlJCYr79MYYc" alt="Personas mayores" />
              </div>
              <div className="benefit-content">
                <span className="benefit-tag">Descubre un mundo de posibilidades para</span>
                <h3>Personas mayores</h3>
                <p>Espacios para mantenerte activo, aprender, compartir y disfrutar experiencias que fortalezcan tu bienestar, alegría y conexión en esta etapa de la vida.</p>
                <button className="benefit-btn">Conocer más</button>
              </div>
            </div>

            <div className="benefit-card">
              <div className="benefit-image">
                <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBde66aruVcBIJpnc1WlcfdOf1yDlK8qOfAPEEtu2ab9eAJKWY144usPxM42H-sAZZW0rQQKYhM5BmRke4nJ-VnUrK2vXLZUUwAAnnsp50zzmbAKVEsIe3fvhXSTyaSOokxOq0IV6q0g8Nr3GMQ1g0YFT3F-kKmsIGU6qBfFPpheusgBOKIWfu_c-Pwd8A-EGkJhDTGMyEm42ZNCXByWDfMB867GrwEqQzXBOcxH4-kaop_M95zduuyMB2MMz1EORKrJWjpC7zuyhVH" alt="Mascotas" />
              </div>
              <div className="benefit-content">
                <span className="benefit-tag">Descubre un mundo de posibilidades para</span>
                <h3>Mascotas</h3>
                <p>Servicios para cuidar, proteger y consentir a tu peludo, fortaleciendo su bienestar y devolviéndole todo el amor que llena tu hogar.</p>
                <button className="benefit-btn">Conocer más</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Locations Section */}
      <section className="locations-section">
        <div className="container-comfama">
          <div className="section-header">
            <span className="section-tag">Encuéntranos en todas las regiones y subregiones de Antioquia</span>
            <h2 className="section-title-dark">Espacios y sedes Comfama</h2>
          </div>
          
          <div className="locations-carousel">
            <div className="locations-track" style={{ transform: `translateX(-${currentLocation * 340}px)` }}>
              {locations.map((location, index) => (
                <div key={index} className="location-card">
                  <div className="location-image">
                    <img src={location.image} alt={location.title} />
                  </div>
                  <h3>{location.title}</h3>
                  <p>{location.description}</p>
                </div>
              ))}
            </div>
            <button className="carousel-btn-comfama prev" onClick={() => scrollLocations('prev')}>‹</button>
            <button className="carousel-btn-comfama next" onClick={() => scrollLocations('next')}>›</button>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="faq-section">
        <div className="container-comfama">
          <div className="faq-wrapper">
            <div className="faq-content">
              <h2>Lo más buscado en Comfama</h2>
              <p>Estas son algunas de las dudas o preguntas más comunes de nuestros usuarios y usuarias.</p>
              
              <div className="tab-selector">
                <button className="tab-btn active">Personas y familias</button>
                <button className="tab-btn">Empresas</button>
              </div>

              <div className="faq-list">
                <div className="faq-item">
                  <span>¿Cómo participar en la reunión ordinaria de afiliados 2024?</span>
                  <span className="faq-icon">+</span>
                </div>
                <div className="faq-item">
                  <span>¿Cómo conocer el estado de mi afiliación Comfama?</span>
                  <span className="faq-icon">+</span>
                </div>
                <div className="faq-item">
                  <span>¿Cómo consultar mi tarifa de afiliado a Comfama?</span>
                  <span className="faq-icon">+</span>
                </div>
                <div className="faq-item">
                  <span>¿Cuáles son los requisitos para solicitar créditos en Comfama?</span>
                  <span className="faq-icon">+</span>
                </div>
              </div>
            </div>
            
            <div className="faq-help">
              <div className="help-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </div>
              <h3>Centro de ayuda Comfama</h3>
              <p>En este espacio podrás encontrar toda la información relacionada con nuestros servicios y programas.</p>
              <a href="#">Ir al Centro de Ayuda</a>
            </div>
          </div>
        </div>
      </section>

      {/* Anniversary Section */}
      <section className="anniversary-section">
        <div className="anniversary-overlay"></div>
        <div className="anniversary-content">
          <h2>¡70 años de Comfama!</h2>
          <p>Celebramos siete décadas de compromiso con los trabajadores, sus familias, las empresas y las regiones de Antioquia.</p>
          <button className="anniversary-btn">Conoce más</button>
        </div>
      </section>
    </div>
  )
}

export default Home
