import anime from 'animejs';

// Scene animation controller
class SceneController {
    constructor() {
        this.currentScene = 1;
        this.scenes = document.querySelectorAll('.scene');
        this.authScenes = document.querySelectorAll('.auth-scene');
        this.lastActivityTime = Date.now();
        this.idleTimer = null;
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.swooshBuffer = null;
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.animateScene1();
        this.setupScrollListeners();
        this.setupButtonListeners();
        this.setupAuthFormListeners();
        this.setupIdleDetection();
        this.loadSound('https://aidalog.github.io/cdn/swoosh.mp3');
    }

    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sceneNumber = Array.from(this.scenes).indexOf(entry.target) + 1;
                    this.animateScene(sceneNumber);
                }
            });
        }, {
            threshold: 0.3
        });

        this.scenes.forEach(scene => {
            observer.observe(scene);
        });

        // Observe auth sub-scenes independently
        const authSceneObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateAuthScene(entry.target.id);
                }
            });
        }, {
            threshold: 0.5 // Trigger when a significant portion of auth scene is visible
        });

        this.authScenes.forEach(authScene => {
            authSceneObserver.observe(authScene);
        });
    }

    animateScene(sceneNumber) {
        switch (sceneNumber) {
            case 1:
                this.animateScene1();
                break;
            case 2:
                this.animateScene2();
                break;
            case 3:
                this.animateScene3();
                break;
            case 4:
                this.animateScene4();
                break;
            case 5:
                this.animateScene5();
                break;
            case 6: // Auth flow scene
                this.animateScene6();
                break;
        }
    }

    animateScene1() {
        const timeline = anime.timeline({
            easing: 'easeOutExpo'
        });

        timeline
            .add({
                targets: '.entrance-content',
                opacity: [0, 1],
                translateY: [30, 0],
                duration: 1000
            })
            .add({
                targets: '.logo',
                scale: [0.8, 1],
                opacity: [0, 1],
                duration: 800,
                delay: 300
            }, '-=500')
            .add({
                targets: '.tagline',
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600
            }, '-=300')
            .add({
                targets: '.entrance-buttons .btn',
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 500,
                delay: anime.stagger(100)
            }, '-=200');
    }

    animateScene2() {
        const timeline = anime.timeline({
            easing: 'easeOutExpo'
        });

        timeline
            .add({
                targets: '.purpose-text',
                opacity: [0, 1],
                translateX: [-50, 0],
                duration: 1000
            })
            .add({
                targets: '.whisper-title',
                opacity: [0, 1],
                duration: 1200,
                delay: anime.stagger(100, { from: 'first' })
            }, '-=800')
            .add({
                targets: '.purpose-animation',
                opacity: [0, 1],
                translateX: [50, 0],
                duration: 1000
            }, '-=800')
            .add({
                targets: '.floating-logbook, .ticking-clock, .auto-form',
                scale: [0.8, 1],
                opacity: [0, 1],
                translateY: [30, 0],
                duration: 600,
                delay: anime.stagger(200)
            }, '-=500');

        // Floating animations for purpose elements
        anime({
            targets: '.floating-logbook',
            translateY: [-10, 10],
            duration: 3000,
            easing: 'easeInOutSine',
            loop: true,
            direction: 'alternate'
        });

        anime({
            targets: '.auto-form',
            translateY: [10, -10],
            duration: 3500,
            easing: 'easeInOutSine',
            loop: true,
            direction: 'alternate',
            delay: 1000
        });
    }

    animateScene3() {
        const timeline = anime.timeline({
            easing: 'easeOutExpo'
        });

        timeline
            .add({
                targets: '.steps-title',
                opacity: [0, 1],
                translateY: [30, 0],
                duration: 800
            })
            .add({
                targets: '.step-card',
                opacity: [0, 1],
                translateY: [30, 0],
                duration: 600,
                delay: anime.stagger(200, { from: 'first' })
            }, '-=400');

        // Ripple effect on hover
        document.querySelectorAll('.step-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                anime({
                    targets: card,
                    scale: [1, 1.02],
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });

            card.addEventListener('mouseleave', () => {
                anime({
                    targets: card,
                    scale: [1.02, 1],
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });
        });
    }

    animateScene4() {
        const timeline = anime.timeline({
            easing: 'easeOutExpo'
        });

        timeline
            .add({
                targets: '.companion-content',
                opacity: [0, 1],
                translateY: [40, 0],
                duration: 1000
            })
            .add({
                targets: '.companion-title',
                opacity: [0, 1],
                scale: [0.95, 1],
                duration: 800
            }, '-=600')
            .add({
                targets: '.companion-subtitle',
                opacity: [0, 1],
                duration: 600
            }, '-=400')
            .add({
                targets: '.companion-buttons .btn',
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 500,
                delay: anime.stagger(100)
            }, '-=300')
            .add({
                targets: '.student-illustration',
                opacity: [0, 0.7],
                scale: [0.8, 1],
                duration: 800
            }, '-=400');
    }

    animateScene5() {
        const timeline = anime.timeline({
            easing: 'easeOutExpo'
        });

        timeline
            .add({
                targets: '.footer-nav',
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600
            })
            .add({
                targets: '.footer-divider',
                opacity: [0, 1],
                scaleX: [0, 1],
                duration: 800
            }, '-=300')
            .add({
                targets: '.closing-quote',
                opacity: [0, 1],
                duration: 800
            }, '-=400');
    }

    animateScene6() {
        // Only animate the login section on initial visibility
        this.animateAuthScene('login-section');
    }

    animateAuthScene(id) {
        const targetScene = document.getElementById(id);
        if (!targetScene) return;

        // Prevent re-animating if already visible and animated
        if (targetScene.dataset.animated === 'true') return;

        anime.timeline({
            easing: 'easeOutExpo'
        })
            .add({
                targets: targetScene,
                opacity: [0, 1],
                translateY: [30, 0],
                duration: 800,
                begin: () => {
                    targetScene.dataset.animated = 'true'; // Mark as animated
                }
            })
            .add({
                targets: targetScene.querySelector('.auth-title'),
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600
            }, '-=500')
            .add({
                targets: targetScene.querySelector('.auth-subtitle'),
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600
            }, '-=300')
            .add({
                targets: targetScene.querySelectorAll('.input-group'),
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 500,
                delay: anime.stagger(150),
                begin: () => {
                    if (id === 'register-section') {
                        this.playSwooshSound(); // Play sound for register inputs
                    }
                }
            }, '-=200')
            .add({
                targets: targetScene.querySelector('.auth-btn'),
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 500
            }, '-=100')
            .add({
                targets: targetScene.querySelectorAll('.auth-micro-text a'),
                opacity: [0, 1],
                translateY: [10, 0],
                duration: 400,
                delay: anime.stagger(50)
            }, '-=200');
    }

    setupScrollListeners() {
        try {
            // Smooth scroll for "Learn How It Works" button
            const learnHowItWorksButton = document.querySelector('.btn.secondary');
            // Check if the button element exists before adding the event listener
            if (learnHowItWorksButton) {
                learnHowItWorksButton.addEventListener('click', () => {
                    document.querySelector('.scene-2').scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            }
        } catch (error) {
            console.error('Error setting up button click sound:', error);
        }

    }

    setupButtonListeners() {
        // Button hover animations & ripple effect (already existing)
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                anime({
                    targets: btn,
                    scale: 1.05,
                    duration: 200,
                    easing: 'easeOutQuad'
                });
            });

            btn.addEventListener('mouseleave', () => {
                anime({
                    targets: btn,
                    scale: 1,
                    duration: 200,
                    easing: 'easeOutQuad'
                });
            });

            btn.addEventListener('click', (e) => {
                // Ripple effect
                const ripple = document.createElement('span');
                const rect = btn.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');

                btn.appendChild(ripple);

                anime({
                    targets: ripple,
                    scale: [0, 2],
                    opacity: [0.5, 0],
                    duration: 600,
                    easing: 'easeOutExpo',
                    complete: () => {
                        ripple.remove();
                    }
                });
            });
        });
    }

    setupAuthFormListeners() {
        document.querySelectorAll('.auth-input').forEach(input => {
            const underline = input.nextElementSibling; // Get the .underline-effect span

            input.addEventListener('focus', () => {
                anime({
                    targets: underline,
                    width: '100%',
                    duration: 300,
                    easing: 'easeOutQuad'
                });
                // For password fields, apply a gentle pulse
                if (input.type === 'password') {
                    anime({
                        targets: input,
                        boxShadow: ['0 0 0 rgba(139, 154, 139, 0)', '0 0 10px rgba(139, 154, 139, 0.3)'],
                        duration: 800,
                        easing: 'easeOutQuad',
                        loop: true,
                        direction: 'alternate'
                    });
                }
            });

            input.addEventListener('blur', () => {
                anime({
                    targets: underline,
                    width: '0%',
                    duration: 300,
                    easing: 'easeOutQuad'
                });
                // Remove pulse for password fields
                if (input.type === 'password') {
                    anime.remove(input); // Stop ongoing animation
                    input.style.boxShadow = 'none'; // Reset box shadow
                }
            });
        });

        // Password mismatch shake for register
        const registerForm = document.querySelector('#register-section .auth-form');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                const password = registerForm.querySelector('#register-password').value;
                const confirmPassword = registerForm.querySelector('#register-confirm-password').value;
                if (password !== confirmPassword) {
                    e.preventDefault();
                    anime({
                        targets: [registerForm.querySelector('#register-password').parentNode, registerForm.querySelector('#register-confirm-password').parentNode],
                        translateX: [
                            { value: -10, duration: 50 },
                            { value: 10, duration: 50 },
                            { value: -10, duration: 50 },
                            { value: 0, duration: 50 }
                        ],
                        easing: 'easeInOutSine'
                    });
                }
            });
        }

        // Reset password button pulse
        const resetButton = document.querySelector('#reset-section .auth-btn');
        if (resetButton) {
            anime({
                targets: resetButton,
                scale: [1, 1.01],
                boxShadow: ['0 8px 25px rgba(139, 154, 139, 0.3)', '0 8px 30px rgba(139, 154, 139, 0.4)'],
                duration: 1500,
                easing: 'easeInOutSine',
                loop: true,
                direction: 'alternate'
            });
        }
    }

    // Sound effect methods
    async loadSound(url) {
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            this.swooshBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
        } catch (error) {
            console.error('Error loading sound:', error);
        }
    }

    playSwooshSound() {
        if (this.swooshBuffer) {
            const source = this.audioContext.createBufferSource();
            source.buffer = this.swooshBuffer;
            source.connect(this.audioContext.destination);
            source.start(0);
        }
    }

    // Idle animation (petals)
    setupIdleDetection() {
        const events = ['mousemove', 'keydown', 'scroll', 'click', 'touchstart'];
        events.forEach(event => {
            document.addEventListener(event, this.resetIdleTimer.bind(this));
        });
        this.startIdleTimer();
    }

    resetIdleTimer() {
        this.lastActivityTime = Date.now();
        clearTimeout(this.idleTimer);
        this.stopPetalAnimation();
        this.startIdleTimer();
    }

    startIdleTimer() {
        this.idleTimer = setTimeout(() => {
            this.triggerPetalAnimation();
        }, 15000); // 15 seconds
    }

    triggerPetalAnimation() {
        const petalContainer = document.querySelector('.auth-petal-bg');
        if (!petalContainer) return;

        for (let i = 0; i < 10; i++) { // Spawn a few petals
            this.createPetal(petalContainer);
        }
    }

    createPetal(container) {
        const petal = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        petal.setAttribute('class', 'petal-svg');
        petal.setAttribute('viewBox', '0 0 20 20');
        petal.style.position = 'absolute';
        petal.style.left = `${Math.random() * 100}vw`;
        petal.style.top = `-${Math.random() * 50}px`; // Start above screen
        petal.style.pointerEvents = 'none';
        petal.style.zIndex = '0';
        petal.style.opacity = '0.8';

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', 'M10 0 Q15 5 20 10 Q15 15 10 20 Q5 15 0 10 Q5 5 10 0Z');
        path.setAttribute('fill', `rgba(255, 200, 200, ${0.4 + Math.random() * 0.4})`); // Pale pink/blush
        path.setAttribute('stroke', `rgba(255, 150, 150, ${0.2 + Math.random() * 0.2})`);
        path.setAttribute('stroke-width', '0.5');
        petal.appendChild(path);
        container.appendChild(petal);

        const duration = 5000 + Math.random() * 3000;
        const delay = Math.random() * 2000;

        anime({
            targets: petal,
            translateY: [0, window.innerHeight + 100], // Fall off screen
            translateX: [0, (Math.random() - 0.5) * 200], // Horizontal drift
            rotate: [0, 360 * (Math.random() > 0.5 ? 1 : -1)], // Spin
            opacity: [0.8, 0],
            easing: 'linear',
            duration: duration,
            delay: delay,
            complete: () => {
                petal.remove();
            }
        });
    }

    stopPetalAnimation() {
        const petalContainer = document.querySelector('.auth-petal-bg');
        if (petalContainer) {
            anime.remove('.petal-svg'); // Stop all animations
            while (petalContainer.firstChild) {
                petalContainer.removeChild(petalContainer.firstChild); // Remove all existing petals
            }
        }
    }
}


// CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        pointer-events: none;
        transform: scale(0);
    }
`;
document.head.appendChild(style);

// Add global styles for petals
const petalStyle = document.createElement('style');
petalStyle.textContent = `
    .petal-svg {
        position: absolute;
        pointer-events: none;
        transform-origin: center center;
        width: 20px;
        height: 20px;
        filter: blur(0.5px); /* Soften petals */
    }
`;
document.head.appendChild(petalStyle);


// Initialize the scene controller when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SceneController();
});

// Add parallax effect to wave pattern
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.wave-pattern');
    if (parallax) {
        const speed = scrolled * 0.2;
        parallax.style.transform = `translateY(${speed}px)`;
    }
});