/**
 * United Cinema - Interactive Features & 5-Second Carousel
 * Location: Centre administratif de Mbankomo - Yaoundé - Cameroun
 */

document.addEventListener('DOMContentLoaded', () => {
  // =========================================================================
  // ROW 4: CAROUSEL WITH EXACTLY 5 SECONDS LAPSE
  // =========================================================================
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  const prevBtn = document.querySelector('.carousel-prev');
  const nextBtn = document.querySelector('.carousel-next');
  const progressFill = document.querySelector('.carousel-progress-fill');
  const carouselContainer = document.querySelector('.carousel-container');

  if (slides.length > 0) {
    let currentSlide = 0;
    const SLIDE_DURATION = 5000; // 5 seconds
    const UPDATE_INTERVAL = 50;  // progress bar update interval in ms
    let elapsedTime = 0;
    let autoSlideTimer = null;
    let isPaused = false;

    function showSlide(index) {
      if (index >= slides.length) {
        currentSlide = 0;
      } else if (index < 0) {
        currentSlide = slides.length - 1;
      } else {
        currentSlide = index;
      }

      slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === currentSlide);
      });

      dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
      });

      elapsedTime = 0;
      if (progressFill) {
        progressFill.style.width = '0%';
      }
    }

    function nextSlide() {
      showSlide(currentSlide + 1);
    }

    function prevSlide() {
      showSlide(currentSlide - 1);
    }

    function startTimer() {
      if (autoSlideTimer) clearInterval(autoSlideTimer);

      autoSlideTimer = setInterval(() => {
        if (!isPaused) {
          elapsedTime += UPDATE_INTERVAL;
          const percentage = Math.min((elapsedTime / SLIDE_DURATION) * 100, 100);
          if (progressFill) {
            progressFill.style.width = `${percentage}%`;
          }

          if (elapsedTime >= SLIDE_DURATION) {
            nextSlide();
          }
        }
      }, UPDATE_INTERVAL);
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        nextSlide();
        elapsedTime = 0;
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        prevSlide();
        elapsedTime = 0;
      });
    }

    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        showSlide(i);
        elapsedTime = 0;
      });
    });

    if (carouselContainer) {
      carouselContainer.addEventListener('mouseenter', () => {
        isPaused = true;
      });

      carouselContainer.addEventListener('mouseleave', () => {
        isPaused = false;
      });

      // Touch / Swipe support
      let touchStartX = 0;
      let touchEndX = 0;

      carouselContainer.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      carouselContainer.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (touchStartX - touchEndX > 50) {
          nextSlide();
        } else if (touchEndX - touchStartX > 50) {
          prevSlide();
        }
      }, { passive: true });
    }

    // Initialize slide & start 5-second interval
    showSlide(0);
    startTimer();
  }

  // =========================================================================
  // ROW 3: LIGHTBOX FOR WEEKLY SCHEDULE IMAGE
  // =========================================================================
  const scheduleFrame = document.querySelector('.schedule-mounted-frame');
  const lightboxModal = document.getElementById('scheduleLightbox');
  const lightboxCloseBtn = document.querySelector('.lightbox-close-btn');

  if (scheduleFrame && lightboxModal) {
    scheduleFrame.addEventListener('click', () => {
      lightboxModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });

    if (lightboxCloseBtn) {
      lightboxCloseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        lightboxModal.classList.remove('active');
        document.body.style.overflow = '';
      });
    }

    lightboxModal.addEventListener('click', (e) => {
      if (e.target === lightboxModal || e.target.classList.contains('lightbox-content')) {
        lightboxModal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightboxModal.classList.contains('active')) {
        lightboxModal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  // =========================================================================
  // MOBILE MENU TOGGLE
  // =========================================================================
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const mainNav = document.querySelector('.main-nav');

  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
      mainNav.classList.toggle('open');
    });

    // Close mobile nav when clicking a link
    mainNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('open');
      });
    });
  }

  // =========================================================================
  // SMOOTH ANCHOR HIGHLIGHTING & SCROLL
  // =========================================================================
  const navLinks = document.querySelectorAll('.main-nav a[href^="#"]');
  window.addEventListener('scroll', () => {
    let currentSectionId = '';
    const sections = document.querySelectorAll('section[id], div[id^="schedule"]');
    
    sections.forEach((section) => {
      const sectionTop = section.offsetTop - 120;
      if (window.scrollY >= sectionTop) {
        currentSectionId = section.getAttribute('id');
      }
    });

    navLinks.forEach((link) => {
      const href = link.getAttribute('href').substring(1);
      link.classList.toggle('active', href === currentSectionId);
    });
  });
});
