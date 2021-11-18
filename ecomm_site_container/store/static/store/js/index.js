let searcharray = [
    "ASIAN Future-01", "ASIAN Wonder-13", "Hravso GRSK", "Neeman's Classics",
    "Lancer Hydra-46", "Converse Basics", "Knoos Reed", "Krasa Neo", "Flite Form",
    "NIVIA Verdict", "Reebok Revolution", "SPARX 414","Symbol Nexus", 
    "Bacca Bucci Steel", "Cebtrio Woods", "Neeman's Slipons", "Puma Starlight",
    "Redchief Woodland", "Red Tape Basics", "Reebok Reetek", "Rook Basics",
    "SPARX 323", "SPARX 402", "Adidas Addilet", "Benneton Evo", "Big Fox FTS",
    "Des Tongs", "Doctor Extras", "Flite FL", "Flite SC", "Perry Pao", "Zappy M1",
    "Soulthreads Freeway", "Zerol Clogs", "Big Fox BFS", "Sparx SF0", "Bata Scale",
    "Bata Edgar", "Alberto Toressi J", "Alberto Torresi K", "Bata Alfred",
    "Stylure Pog", "Red Tape Nine", "Red Tape 91", "Mactree K10", "Bata Lace",
    "Bata SA05", "Centrino Original", "Centrino M", "Shoemate Slides",
    "Bourge Loire-z126", "Campus Gilbert", "Campus Oxyfit", "Campus Rodeo-2",
    "Campus S-Cross", "Campus Stonic", "Redchief FURO-5", "Redchief FURO-4",
    "Redchief FURO-7"
  ];
  
  const searchInput = document.getElementById('inputbar');
  const searchbar = document.querySelector('.searchbar');
  const resultsbar = document.querySelector('.results');
  
  searchInput.addEventListener('keyup', () => {
    let results = [];
    let input = searchInput.value;
    if (input.length) {
      results = searcharray.filter((item) => {
        return item.toLowerCase().includes(input.toLowerCase());
      });
    }
    renderResults(results);
  });
  
  function renderResults(results) {
    if (!results.length) {
      return searchbar.classList.remove('show');
    }
  
    const content = results
      .map((item) => {
        return `<li>${item}</li>`;
      })
      .join('');
  
    searchbar.classList.add('show');
    resultsbar.innerHTML = `<ul>${content}</ul>`;
  }
  
gsap.from(".logo", { opacity: 0, duration: 1, delay: 0.5, y: -10 });
gsap.from(".hamburger", { opacity: 0, duration: 1, delay: 1, x: 20 });
gsap.from(".h1", { opacity: 0, duration: 1, delay: 1.5, x: -200 });
gsap.from(".img-content h2", { opacity: 0, duration: 1, delay: 2, y: -50 });
gsap.from(".img-content h1", { opacity: 0, duration: 1, delay: 2.5, y: -45 });
gsap.from(".gimg", { opacity: 0, duration: 1, delay: 2.5, x: -45 });
gsap.from(".img-content a", { opacity: 0, duration: 1, delay: 3.5, y: 50 });
gsap.from(".box", { opacity: 0, duration: 0.5, delay: 1, x: -100 });
