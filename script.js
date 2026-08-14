// ========================================
//   IKON COMPUTER EDUCATION - Main Script
// ========================================

// ===== LIGHTBOX (Brochure image zoom) =====
function openLightbox() {
  const lb = document.getElementById('lightbox');
  if (lb) {
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeLightbox() {
  const lb = document.getElementById('lightbox');
  if (lb) {
    lb.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// Close lightbox with Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeLightbox();
});

// ===== PAYMENT SECTION =====

// Switch between UPI and NEFT tabs
function switchPayTab(tab) {
  document.querySelectorAll('.pay-tab').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.pay-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('ptab-'   + tab).classList.add('active');
  document.getElementById('ppanel-' + tab).classList.add('active');
}

// Copy UPI ID to clipboard
function copyUPI() {
  const id  = document.getElementById('upi-id-text').textContent.trim();
  const btn = document.getElementById('copy-upi-btn');
  const lbl = document.getElementById('copy-label');

  navigator.clipboard.writeText(id).then(() => {
    lbl.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {
      lbl.textContent = 'Copy';
      btn.classList.remove('copied');
    }, 2500);
  }).catch(() => {
    // Fallback for browsers without clipboard API
    const ta = document.createElement('textarea');
    ta.value = id;
    ta.style.position = 'fixed';
    ta.style.opacity  = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    lbl.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {
      lbl.textContent = 'Copy';
      btn.classList.remove('copied');
    }, 2500);
  });
}

// Copy any text (used for NEFT bank details click-to-copy)
function copyText(text, el) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = el.innerHTML;
    el.innerHTML = '&#10003; Copied!';
    el.style.color = 'var(--accent-green)';
    setTimeout(() => {
      el.innerHTML = orig;
      el.style.color = '';
    }, 2000);
  }).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  });
}

// ===== NAVBAR SCROLL EFFECT =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// ===== HAMBURGER MENU =====
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  const spans = hamburger.querySelectorAll('span');
  if (navLinks.classList.contains('open')) {
    spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
    spans[1].style.opacity = '0';
    spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
  } else {
    spans.forEach(s => {
      s.style.transform = '';
      s.style.opacity = '';
    });
  }
});

// Close nav on link click (mobile)
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.querySelectorAll('span').forEach(s => {
      s.style.transform = '';
      s.style.opacity = '';
    });
  });
});

// ===== FAQ ACCORDION =====
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  const isOpen = item.classList.contains('open');

  // Close all
  document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

  // Open clicked (if it wasn't open)
  if (!isOpen) {
    item.classList.add('open');
  }
}

// ===== REGISTRATION ENDPOINT =====
// Since GitHub Pages is static, we will mock the backend using localStorage.
// This allows the website to function perfectly as a demo without throwing server errors.
const GOOGLE_SCRIPT_URL = 'LOCAL_STORAGE';

// ===== FORM SUBMISSION → LOCAL STORAGE =====
async function handleSubmit(event) {
  event.preventDefault();

  const btn = document.getElementById('form-submit');
  btn.textContent = 'Submitting…';
  btn.disabled = true;

  // Collect form values
  const payload = {
    id: 'REG-' + Math.floor(Math.random() * 90000 + 10000),
    timestamp:  new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }),
    name:       document.getElementById('input-name').value.trim(),
    email:      document.getElementById('input-email').value.trim(),
    phone:      document.getElementById('input-phone').value.trim(),
    course:     document.getElementById('input-course').value,
    mode:       document.getElementById('input-mode').value,
    message:    document.getElementById('input-message').value.trim(),
  };

  // Simulate network delay
  setTimeout(() => {
    try {
      // Save to localStorage
      const registrations = JSON.parse(localStorage.getItem('ikon_registrations') || '[]');
      registrations.push(payload);
      localStorage.setItem('ikon_registrations', JSON.stringify(registrations));
      
      showSuccess(btn, payload);
    } catch (err) {
      console.error('Registration error:', err);
      showFormError(btn, 'Could not save registration. Please try again.');
    }
  }, 1000);
}

// After successful registration → redirect to login page with email pre-filled
function showSuccess(btn, payload) {
  btn.textContent = 'Submit Application →';
  btn.disabled = false;
  document.getElementById('register-form').reset();

  // Build login URL with pre-filled email & name so the student can log in immediately
  const loginUrl = 'login.html'
    + '?email=' + encodeURIComponent(payload.email)
    + '&name='  + encodeURIComponent(payload.name);

  // Brief confirmation before redirect
  const formSection = document.getElementById('register');
  if (formSection) {
    const msg = document.createElement('div');
    msg.style.cssText = [
      'position:fixed', 'top:50%', 'left:50%',
      'transform:translate(-50%,-50%)',
      'background:white', 'border-radius:20px',
      'padding:36px 40px', 'text-align:center',
      'box-shadow:0 20px 60px rgba(0,0,0,.2)',
      'z-index:9999', 'max-width:380px', 'width:90%',
      'animation:fadeInScale .3s ease'
    ].join(';');
    msg.innerHTML = [
      '<div style="font-size:52px;margin-bottom:12px">&#127881;</div>',
      '<h3 style="font-family:Outfit,sans-serif;font-size:22px;font-weight:800;margin-bottom:8px">',
        'Registration Successful!',
      '</h3>',
      '<p style="font-size:14px;color:#6b7280;line-height:1.6;margin-bottom:20px">',
        'Welcome, <strong>' + payload.name + '</strong>! Taking you to your student portal…',
      '</p>',
      '<div style="width:40px;height:4px;background:linear-gradient(90deg,#1a73e8,#FF6B35);',
        'border-radius:2px;margin:0 auto;animation:grow 1.5s ease forwards"></div>'
    ].join('');

    // Overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.5);backdrop-filter:blur(6px);z-index:9998';
    document.body.appendChild(overlay);
    document.body.appendChild(msg);
  }

  setTimeout(() => { window.location.href = loginUrl; }, 2000);
}

// Show inline error under the submit button (no alert() popup)
function showFormError(btn, message) {
  btn.textContent = 'Submit Application →';
  btn.disabled = false;
  let errEl = document.getElementById('form-submit-error');
  if (!errEl) {
    errEl = document.createElement('p');
    errEl.id = 'form-submit-error';
    errEl.style.cssText = [
      'margin-top:10px', 'padding:10px 14px',
      'background:#ffebee', 'border:1px solid #ef9a9a',
      'border-radius:8px', 'color:#b71c1c',
      'font-size:13px', 'line-height:1.5', 'text-align:center'
    ].join(';');
    btn.parentNode.insertBefore(errEl, btn.nextSibling);
  }
  errEl.textContent = message;
  errEl.style.display = 'block';
  setTimeout(() => { errEl.style.display = 'none'; }, 8000);
}

function closeModal() {
  document.getElementById('success-modal').classList.remove('show');
}

// Close modal on overlay click
document.getElementById('success-modal').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) closeModal();
});

// Close modal on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

// ===== SCROLL ANIMATIONS (Intersection Observer) =====
const fadeElements = document.querySelectorAll(
  '.feature-card, .course-card, .testimonial-card, .process-step, .faq-item, .highlight-item'
);

fadeElements.forEach(el => el.classList.add('fade-in'));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, index * 80);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

fadeElements.forEach(el => observer.observe(el));

// ===== COUNTER ANIMATION =====
function animateCounter(el, target, suffix = '') {
  let current = 0;
  const step = target / 60;
  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = Math.floor(current) + suffix;
  }, 25);
}

// Stats counter (triggers when visible)
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const stats = entry.target.querySelectorAll('.stat-num');
      stats.forEach(stat => {
        const text = stat.textContent;
        if (text.includes('2000')) animateCounter(stat, 2000, '+');
        else if (text === '4') animateCounter(stat, 4, '');
        else if (text.includes('95')) animateCounter(stat, 95, '%');
      });
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) statsObserver.observe(heroStats);

// About stats counter
const aboutStatsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const nums = entry.target.querySelectorAll('.ach-num');
      nums.forEach(num => {
        const text = num.textContent;
        if (text.includes('2000')) animateCounter(num, 2000, '+');
        else if (text.includes('10')) animateCounter(num, 10, '+');
        else if (text.includes('95')) animateCounter(num, 95, '%');
        else if (text.includes('50')) animateCounter(num, 50, '+');
      });
      aboutStatsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const aboutStats = document.querySelector('.about-stats-card');
if (aboutStats) aboutStatsObserver.observe(aboutStats);

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ===== ACTIVE NAV LINK HIGHLIGHT =====
const sections = document.querySelectorAll('section[id]');
const navLinksAll = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 100;
    if (window.pageYOffset >= sectionTop) {
      current = section.getAttribute('id');
    }
  });

  navLinksAll.forEach(link => {
    link.style.color = '';
    const href = link.getAttribute('href');
    if (href && href.includes(current)) {
      link.style.color = 'var(--blue-primary)';
    }
  });
});

// ===== BROCHURE DOWNLOAD SIMULATION =====


// ===== TYPING ANIMATION FOR HERO =====
const heroTitle = document.querySelector('.hero-title');
const phrases = ['Java', 'Python', 'DBMS', 'Networking'];
let phraseIndex = 0;

// ===== PARALLAX SHAPES =====
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  const shapes = document.querySelectorAll('.shape');
  shapes.forEach((shape, i) => {
    const speed = (i + 1) * 0.05;
    shape.style.transform = `translateY(${scrollY * speed}px)`;
  });
});

// ===== COURSE CARD HOVER GLOW =====
document.querySelectorAll('.course-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    card.style.background = `radial-gradient(circle at ${x}% ${y}%, rgba(26,115,232,0.04) 0%, white 60%)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.background = '';
  });
});

// ===== SEARCH BUTTON =====
document.getElementById('nav-search').addEventListener('click', () => {
  const query = prompt('Search courses (e.g. Java, Python, DBMS, Networking):');
  if (query) {
    const courseMap = {
      java: '#java',
      python: '#python',
      dbms: '#dbms',
      database: '#dbms',
      networking: '#networking',
      network: '#networking',
    };
    const key = query.toLowerCase().trim();
    for (const [term, anchor] of Object.entries(courseMap)) {
      if (key.includes(term)) {
        document.querySelector(anchor)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
    }
    alert('No exact match found. Browse our Courses section below!');
    document.querySelector('#courses')?.scrollIntoView({ behavior: 'smooth' });
  }
});

console.log('%c🎓 Ikon Computer Education & Training Institute', 'color:#1a73e8;font-size:16px;font-weight:bold;');
console.log('%cBuilt with ❤️ | MSME Verified | ISO Certified', 'color:#FF6B35;font-size:12px;');

// ===== CHATBOT LOGIC =====
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotWindow = document.getElementById('chatbot-window');
const chatClose = document.getElementById('chat-close');
const chatBody = document.getElementById('chat-body');
const chatInput = document.getElementById('chat-input');

if (chatbotToggle && chatbotWindow) {
  chatbotToggle.addEventListener('click', () => {
    chatbotWindow.classList.add('open');
    chatInput.focus();
  });

  chatClose.addEventListener('click', () => {
    chatbotWindow.classList.remove('open');
  });
}

function handleChatEnter(event) {
  if (event.key === 'Enter') {
    sendChatMessage();
  }
}

function sendQuickReply(text) {
  chatInput.value = text;
  sendChatMessage();
}

function sendChatMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  // Add user message
  appendMessage(text, 'user');
  chatInput.value = '';

  // Simulate typing delay
  setTimeout(() => {
    const responseData = getBotResponse(text.toLowerCase());
    appendMessage(responseData.text, 'bot', responseData.allied);
  }, 500);
}

function appendMessage(htmlContent, sender, alliedQuestions = []) {
  const msgWrap = document.createElement('div');
  msgWrap.style.display = 'flex';
  msgWrap.style.flexDirection = 'column';
  msgWrap.style.alignItems = sender === 'user' ? 'flex-end' : 'flex-start';
  
  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-msg ${sender}`;
  msgDiv.innerHTML = htmlContent;
  msgWrap.appendChild(msgDiv);

  if (sender === 'bot' && alliedQuestions && alliedQuestions.length > 0) {
    const chipsDiv = document.createElement('div');
    chipsDiv.className = 'chat-chips';
    chipsDiv.style.marginTop = '6px';
    chipsDiv.style.marginLeft = '4px';
    alliedQuestions.forEach(q => {
      const chip = document.createElement('span');
      chip.className = 'chat-chip';
      chip.textContent = q;
      chip.onclick = () => sendQuickReply(q);
      chipsDiv.appendChild(chip);
    });
    msgWrap.appendChild(chipsDiv);
  }

  chatBody.appendChild(msgWrap);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function getBotResponse(input) {
  // Check specific queries first (duration, fees, prospect, cert)
  if (input.includes('duration') || input.includes('time') || input.includes('how long') || input.includes('month') || input.includes('days')) {
    return {
      text: 'The duration for each of our intensive internship courses is <strong>1 Month (30 Days)</strong>.',
      allied: ['Course fees', 'Courses offered', 'Internship prospects']
    };
  }
  if (input.includes('fee') || input.includes('cost') || input.includes('price') || input.includes('pay') || input.includes('1000')) {
    return {
      text: 'The fee for each course is incredibly affordable at just <strong>Rs. 1000/-</strong>.',
      allied: ['Course duration', 'Certifications', 'How to register?']
    };
  }
  if (input.includes('certif') || input.includes('msme') || input.includes('iso') || input.includes('govt')) {
    return {
      text: 'Our certification system is fully accredited. You will receive certificates that are:<ul><li>✅ MSME Verified</li><li>✅ ISO Certified</li><li>✅ Government-Recognized</li></ul>',
      allied: ['Internship prospects', 'Courses offered', 'Course fees']
    };
  }
  if (input.includes('prospect') || input.includes('placement') || input.includes('job') || input.includes('career') || input.includes('offer letter')) {
    return {
      text: 'The prospects are excellent! You will receive:<ul><li>📄 An Official Offer Letter</li><li>💼 Placement Support & Assistance</li><li>🚀 Hands-on Major Project experience</li></ul>',
      allied: ['Certifications', 'Course fees', 'How to register?']
    };
  }
  if (input.includes('register') || input.includes('apply') || input.includes('join') || input.includes('enroll')) {
    return {
      text: 'You can easily register by closing this chat and clicking the "Register Now" button at the top of the page!',
      allied: ['Courses offered', 'Course fees']
    };
  }
  
  // Specific course subjects
  if (input.includes('java')) {
    return {
      text: 'Our ☕ <strong>Java Programming</strong> internship covers Core Java, OOP Concepts, Arrays & Exception Handling, and Database Connectivity (JDBC). It is perfect for building robust backend applications.',
      allied: ['Course duration', 'Python', 'DBMS', 'Course fees']
    };
  }
  if (input.includes('python')) {
    return {
      text: 'Our 🐍 <strong>Python Development</strong> internship covers Python Basics, Control Structures, Data Structures (Lists, Dictionaries), and File Handling. It is great for automation and backend development!',
      allied: ['Course duration', 'Java', 'Course fees']
    };
  }
  if (input.includes('dbms') || input.includes('database') || input.includes('sql')) {
    return {
      text: 'Our 🗃️ <strong>DBMS</strong> internship teaches you Relational Models, SQL Basics, Database Normalization (1NF to BCNF), and Transaction Management. You will master how to structure and query databases efficiently.',
      allied: ['Course duration', 'Java', 'Python']
    };
  }
  if (input.includes('network')) {
    return {
      text: 'Our 🌐 <strong>Computer Networking</strong> internship dives deep into the OSI Model, TCP/IP Protocol Suite, IP Addressing & Subnetting, and Network Security Fundamentals.',
      allied: ['Course duration', 'Course fees', 'Certifications']
    };
  }
  
  // General course query
  if (input.includes('course') || input.includes('internship')) {
    return {
      text: 'We offer 4 intensive internship courses:<ul><li>☕ Java Programming</li><li>🐍 Python Development</li><li>🗃️ DBMS</li><li>🌐 Computer Networking</li></ul>',
      allied: ['Tell me about Java', 'Tell me about Python', 'DBMS details', 'Course duration']
    };
  }
  
  if (input.includes('hi') || input.includes('hello') || input.includes('hey')) {
    return {
      text: 'Hello there! 👋 How can I assist you with our internship programs today?',
      allied: ['Courses offered', 'Course fees', 'Certifications']
    };
  }
  if (input.includes('thank')) {
    return {
      text: 'You\'re very welcome! Let me know if you have any other questions.',
      allied: []
    };
  }
  
  return {
    text: 'I\'m not entirely sure about that. Could you ask about our <strong>courses</strong>, <strong>duration</strong>, <strong>fees</strong>, <strong>certifications</strong>, or <strong>prospects</strong>?',
    allied: ['Courses offered', 'Course fees', 'Internship prospects']
  };
}

// ===== BACKGROUND MUSIC LOGIC =====
const bgMusic = document.getElementById('bg-music');
const musicToggle = document.getElementById('music-toggle');

if (bgMusic && musicToggle) {
  // Lower the volume slightly since it's background music
  bgMusic.volume = 0.4;

  musicToggle.addEventListener('click', () => {
    if (bgMusic.paused) {
      bgMusic.play();
      musicToggle.classList.add('playing');
    } else {
      bgMusic.pause();
      musicToggle.classList.remove('playing');
    }
  });
}
