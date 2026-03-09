<template>
  <footer class="footer-container">
    <div class="footer-content">
      
    </div>

    <div class="footer-bottom">
     
    </div>
  </footer>
</template>

<script setup>
import { ref, reactive } from "vue";
</script>

<style scoped>
.footer-container {
  background: linear-gradient(135deg, #1a2a6c 0%, #2c3e50 100%);
  color: #ffffff;
  padding: 40px 20px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.footer-logo {
  margin-bottom: 24px;
}

.logo-text {
  display: block;
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: -1px;
  background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.tagline {
  font-size: 1rem;
  color: #a0d8f1;
  font-weight: 400;
  opacity: 0.9;
}

.footer-stats {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.stat-item {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.stat-number {
  display: block;
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 4px;
  background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 0.9rem;
  color: #b3e0ff;
  font-weight: 400;
  opacity: 0.8;
}

.footer-cta {
  margin-bottom: 20px;
}

.cta-text {
  font-size: 1.1rem;
  color: #e0f2ff;
  line-height: 1.6;
  font-style: italic;
  max-width: 600px;
  margin: 0 auto;
  padding: 0 16px;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 16px;
}

.copyright {
  font-size: 0.9rem;
  color: #8fbfff;
  opacity: 0.7;
  letter-spacing: 0.5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer-content {
    padding: 0 20px;
  }

  .footer-stats {
    gap: 20px;
  }

  .stat-number {
    font-size: 1.4rem;
  }

  .stat-label {
    font-size: 0.85rem;
  }

  .cta-text {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .footer-logo {
    margin-bottom: 16px;
  }

  .logo-text {
    font-size: 1.8rem;
  }

  .footer-stats {
    flex-direction: column;
    align-items: center;
  }

  .stat-item {
    margin-bottom: 12px;
  }
}
</style>