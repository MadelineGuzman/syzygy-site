const siteNav = document.getElementById("siteNav");
const navBurger = document.getElementById("navBurger");
const navLinks = document.getElementById("navLinks");
const currentPage = window.location.pathname.split("/").pop() || "index.html";

const updateNavScroll = () => {
  if (!siteNav) {
    return;
  }

  siteNav.classList.toggle("scrolled", window.scrollY > 40);
};

updateNavScroll();
window.addEventListener("scroll", updateNavScroll, { passive: true });

document.querySelectorAll("#navLinks a").forEach((link) => {
  const linkPage = new URL(link.getAttribute("href"), window.location.href).pathname.split("/").pop();

  if (linkPage === currentPage) {
    link.classList.add("active");
  }
});

if (navBurger && navLinks) {
  navBurger.setAttribute("aria-expanded", "false");

  navBurger.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    navBurger.classList.toggle("is-open", isOpen);
    navBurger.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("is-open");
      navBurger.classList.remove("is-open");
      navBurger.setAttribute("aria-expanded", "false");
    });
  });
}

const filterTabs = document.querySelectorAll(".filter-tab");
const projectCards = document.querySelectorAll(".project-card[data-category]");

if (filterTabs.length && projectCards.length) {
  filterTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const activeFilter = tab.dataset.filter;

      filterTabs.forEach((item) => item.classList.toggle("active", item === tab));

      projectCards.forEach((card) => {
        const shouldShow = activeFilter === "all" || card.dataset.category === activeFilter;
        card.classList.toggle("is-hidden", !shouldShow);
      });
    });
  });
}

const contactForm = document.getElementById("contactForm");
const formStatus = document.getElementById("formStatus");

if (contactForm && formStatus) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitButton = contactForm.querySelector("button[type='submit']");
    const formData = new FormData(contactForm);

    formStatus.classList.remove("is-error");
    formStatus.textContent = "";

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Sending...";
    }

    try {
      const response = await fetch(contactForm.action, {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Form submission failed");
      }

      contactForm.reset();
      formStatus.textContent = "Transmission received. I'll be in touch within 48 hours.";
    } catch (error) {
      formStatus.classList.add("is-error");
      formStatus.textContent = "Transmission could not be sent yet. Please replace the Formspree placeholder ID and try again.";
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = "Send Transmission";
      }
    }
  });
}

const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("visible"));
}

function initGate() {
  const gate = document.getElementById("portalGate");

  if (!gate) {
    return;
  }

  const storage = {
    get(key) {
      try {
        return window.localStorage.getItem(key);
      } catch (error) {
        return null;
      }
    },
    set(key, value) {
      try {
        window.localStorage.setItem(key, value);
      } catch (error) {
        // Ignore storage failures so the gate can still run.
      }
    },
  };

  if (storage.get("syzygy_entered") === "true") {
    gate.style.display = "none";
    return;
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    gate.style.display = "none";
    return;
  }

  const canvas = document.getElementById("spaceCanvas");
  const btn = document.getElementById("gateEnterBtn");
  const skip = document.getElementById("gateSkip");

  if (!canvas || !btn || !skip) {
    return;
  }

  const ctx = canvas.getContext("2d");

  if (!ctx) {
    return;
  }

  const resizeCanvas = () => {
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.floor(window.innerWidth * ratio);
    canvas.height = Math.floor(window.innerHeight * ratio);
    canvas.style.width = `${window.innerWidth}px`;
    canvas.style.height = `${window.innerHeight}px`;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    return { width: window.innerWidth, height: window.innerHeight };
  };

  let { width: W, height: H } = resizeCanvas();
  let isHovering = false;
  let isWarping = false;
  let warpStart = null;
  let animFrame;

  const STAR_COUNT = 220;
  const stars = Array.from({ length: STAR_COUNT }, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    z: Math.random() * W,
    size: Math.random() * 1.6 + 0.3,
    opacity: Math.random() * 0.7 + 0.2,
    opacityDir: Math.random() > 0.5 ? 1 : -1,
    vx: (Math.random() - 0.5) * 0.18,
    vy: (Math.random() - 0.5) * 0.18,
  }));

  function drawStars(speedMultiplier, warpProgress) {
    ctx.clearRect(0, 0, W, H);

    stars.forEach((star) => {
      star.opacity += 0.004 * star.opacityDir;

      if (star.opacity > 0.9 || star.opacity < 0.15) {
        star.opacityDir *= -1;
      }

      if (isWarping && warpProgress > 0) {
        const cx = W / 2;
        const cy = H / 2;
        const dx = star.x - cx;
        const dy = star.y - cy;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const warpSpeed = warpProgress * 18;
        const stretch = warpProgress * 12;

        star.x += (dx / dist) * warpSpeed;
        star.y += (dy / dist) * warpSpeed;

        ctx.beginPath();
        ctx.strokeStyle = `rgba(255,255,255,${Math.min(star.opacity + warpProgress * 0.5, 1)})`;
        ctx.lineWidth = star.size * (1 + warpProgress * 2);
        ctx.moveTo(star.x, star.y);
        ctx.lineTo(star.x - (dx / dist) * stretch, star.y - (dy / dist) * stretch);
        ctx.stroke();

        if (star.x < -50 || star.x > W + 50 || star.y < -50 || star.y > H + 50) {
          star.x = cx + (Math.random() - 0.5) * 80;
          star.y = cy + (Math.random() - 0.5) * 80;
        }
      } else {
        const speed = isHovering ? speedMultiplier * 3.5 : 1;
        star.x += star.vx * speed;
        star.y += star.vy * speed;

        if (star.x < 0) star.x = W;
        if (star.x > W) star.x = 0;
        if (star.y < 0) star.y = H;
        if (star.y > H) star.y = 0;

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${star.opacity})`;
        ctx.fill();
      }
    });
  }

  let hoverSpeed = 1;

  function animate(timestamp) {
    if (isWarping) {
      if (!warpStart) {
        warpStart = timestamp;
      }

      const elapsed = timestamp - warpStart;
      const warpProgress = Math.min(elapsed / 1200, 1);
      drawStars(1, warpProgress);

      if (warpProgress >= 1) {
        gate.style.animation = "gateWarpFade 0.5s ease forwards";

        setTimeout(() => {
          gate.style.display = "none";
          storage.set("syzygy_entered", "true");
          const target = document.getElementById("identitySection");

          if (target) {
            target.scrollIntoView({ behavior: "smooth" });
          }
        }, 500);

        cancelAnimationFrame(animFrame);
        return;
      }
    } else {
      if (isHovering && hoverSpeed < 4) hoverSpeed += 0.08;
      if (!isHovering && hoverSpeed > 1) hoverSpeed -= 0.05;
      drawStars(hoverSpeed, 0);
    }

    animFrame = requestAnimationFrame(animate);
  }

  animFrame = requestAnimationFrame(animate);

  btn.addEventListener("mouseenter", () => {
    isHovering = true;
  });

  btn.addEventListener("mouseleave", () => {
    isHovering = false;
  });

  btn.addEventListener(
    "touchstart",
    () => {
      isHovering = true;
    },
    { passive: true }
  );

  btn.addEventListener(
    "touchend",
    () => {
      isHovering = false;
    },
    { passive: true }
  );

  btn.addEventListener("click", () => {
    isWarping = true;
    isHovering = false;
  });

  skip.addEventListener("click", () => {
    gate.style.transition = "opacity 0.3s ease";
    gate.style.opacity = "0";

    setTimeout(() => {
      gate.style.display = "none";
      storage.set("syzygy_entered", "true");
    }, 300);

    cancelAnimationFrame(animFrame);
  });

  window.addEventListener("resize", () => {
    ({ width: W, height: H } = resizeCanvas());
  });

  // Nav brand click triggers gate again from homepage
  const navBrand = document.getElementById("navBrandHome");
  if (navBrand) {
    navBrand.addEventListener("click", (e) => {
      e.preventDefault();
      stars.forEach((star) => {
        star.x = Math.random() * W;
        star.y = Math.random() * H;
        star.opacity = Math.random() * 0.7 + 0.2;
      });
      isWarping = false;
      warpStart = null;
      hoverSpeed = 1;
      gate.style.display = "flex";
      gate.style.opacity = "1";
      gate.style.transition = "none";
      gate.style.animation = "none";
      cancelAnimationFrame(animFrame);
      animFrame = requestAnimationFrame(animate);
      window.scrollTo(0, 0);
    });
  }
}

document.addEventListener("DOMContentLoaded", initGate);
