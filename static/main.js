document.addEventListener("DOMContentLoaded", () => {
  // Tüm şifreleme/deşifreleme butonlarını seç
  const buttons = document.querySelectorAll(".algo-btn");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const algo = button.dataset.algo;  
      const mode = button.dataset.mode; 

      if (!algo || !mode) return;

      // Yönlendirme: encrypt -> ana sayfadan ilgili HTML, decrypt -> sunucu sayfasından ilgili HTML
      if (mode === "encrypt") {
        window.location.href = `/${algo}`;      
      } else if (mode === "decrypt") {
        window.location.href = `/server/${algo}`;   
      }
    });
  });
});
