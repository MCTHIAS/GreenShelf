document.addEventListener('DOMContentLoaded', () => {
    const navMenu = document.querySelector('nav.menu');
    
    // Se não houver um menu nesta página, o script para aqui.
    if (!navMenu) {
        return;
    }

    const links = navMenu.querySelectorAll('a');
    const indicator = navMenu.querySelector('span');

    // Se não encontrar os links ou o indicador, não faz nada.
    if (links.length === 0 || !indicator) {
        return;
    }

    // Função que move e redimensiona o span (o fundo escuro)
    function moveIndicator(targetElement) {
        if (targetElement) {
            indicator.style.left = `${targetElement.offsetLeft}px`;
            indicator.style.width = `${targetElement.offsetWidth}px`;
            // Deixa o texto do link ativo branco
            links.forEach(link => link.style.color = '#2E373A');
            targetElement.style.color = '#FFFFFF';
        }
    }

    // Encontra o link que corresponde à página atual
    let activeLink = Array.from(links).find(link => link.pathname === window.location.pathname);
    
    // Caso especial: se estiver na página inicial, considera o primeiro link como ativo
    if (window.location.pathname === '/') {
        activeLink = links[0];
    }


    // Define a posição inicial do indicador na página ativa
    if (activeLink) {
        // Um pequeno atraso garante que o navegador já calculou o tamanho dos elementos
        setTimeout(() => {
            moveIndicator(activeLink);
            // Garante que a transição só seja ativada após o posicionamento inicial
            indicator.style.transition = 'all 0.4s cubic-bezier(0.23, 1, 0.32, 1)';
        }, 100);
    }

    // Para cada link no menu, adiciona um evento de "mouse enter"
    links.forEach(link => {
        link.addEventListener('mouseenter', () => {
            moveIndicator(link); // Move o indicador para o link onde o mouse está
        });
    });

    // Adiciona um evento de "mouse leave" para o menu inteiro
    navMenu.addEventListener('mouseleave', () => {
        // Quando o mouse sai, move o indicador de volta para o link da página ativa
        moveIndicator(activeLink);
    });
});