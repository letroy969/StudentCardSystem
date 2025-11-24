// Button Glow Effect - Mouse Following
// Applies to all buttons with .button-glow-wrapper class

document.addEventListener('DOMContentLoaded', function() {
    initButtonGlow();
});

function initButtonGlow() {
    const glowElements = document.querySelectorAll('.button-glow');
    
    if (!glowElements.length) return;
    
    glowElements.forEach((glow) => {
        const wrapper = glow.closest('.button-glow-wrapper');
        if (!wrapper) return;
        
        const onMove = (e) => {
            const rect = wrapper.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            glow.style.transform = `translate(-${50 - (x - 50) / 5}%, -${50 - (y - 50) / 5}%)`;
        };
        
        wrapper.addEventListener('mousemove', onMove);
        wrapper.addEventListener('mouseleave', () => {
            glow.style.transform = 'translate(-50%, -50%)';
        });
    });
}

