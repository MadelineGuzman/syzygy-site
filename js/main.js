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
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}
