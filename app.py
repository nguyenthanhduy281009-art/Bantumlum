import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Cấu hình trang
st.set_page_config(page_title="Refined Spray - Duy", layout="wide")

if 'bg_base64' not in st.session_state:
    st.session_state.bg_base64 = ""

# --- SIDEBAR ---
st.sidebar.title("🔫 Refined Spray Studio")
uploaded_file = st.sidebar.file_uploader("👤 Tải ảnh người", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.session_state.bg_base64 = base64.b64encode(uploaded_file.read()).decode()

# Cho phép Duy chỉnh độ ít/nhiều của tia bắn
spray_density = st.sidebar.slider("📉 Lượng tia bắn", 1, 5, 2)
p_size = st.sidebar.slider("💧 Cỡ giọt", 1, 10, 4)

if st.sidebar.button("🧹 DỌN SẠCH"):
    st.rerun()

img_data = f"data:image/png;base64,{st.session_state.bg_base64}" if st.session_state.bg_base64 else ""

# --- HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #000; }}
        #bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{img_data}');
            background-size: contain; background-repeat: no-repeat; background-position: center;
            z-index: 1;
        }}
        canvas {{ position: absolute; top: 0; left: 0; z-index: 2; cursor: crosshair; }}
        
        #source-tool {{
            position: fixed; bottom: -10px; left: 50%; transform: translateX(-50%);
            width: 80px; z-index: 3; pointer-events: none; opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <img id="source-tool" src="https://cdn-icons-png.flaticon.com/512/1023/1023656.png">
    <canvas id="sprayCanvas"></canvas>

    <script>
        const canvas = document.getElementById('sprayCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouse = {{ x: 0, y: 0, down: false }};

        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}

        class Particle {{
            constructor(targetX, targetY) {{
                this.x = canvas.width / 2;
                this.y = canvas.height - 40;
                
                const dx = targetX - this.x;
                const dy = targetY - this.y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                
                // Tốc độ bay nhanh nhưng mảnh hơn
                const force = 25; 
                this.vx = (dx / dist) * force + (Math.random() - 0.5) * 3;
                this.vy = (dy / dist) * force + (Math.random() - 0.5) * 3;
                
                this.size = Math.random() * {p_size} + 1;
                this.gravity = 0.2;
                this.alpha = 1;
                this.decay = 0.012; // Biến mất nhanh hơn để không bị đầy màn hình
            }}

            update() {{
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.alpha -= this.decay;
            }}

            draw() {{
                ctx.fillStyle = `rgba(255, 255, 250, ${{this.alpha}})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        function handleInput(e) {{
            const x = e.clientX || (e.touches && e.touches[0].clientX);
            const y = e.clientY || (e.touches && e.touches[0].clientY);
            mouse.x = x;
            mouse.y = y;
        }}

        window.addEventListener('mousedown', (e) => {{ mouse.down = true; handleInput(e); }});
        window.addEventListener('mouseup', () => mouse.down = false);
        window.addEventListener('mousemove', handleInput);
        
        window.addEventListener('touchstart', (e) => {{ mouse.down = true; handleInput(e); }}, {{passive: false}});
        window.addEventListener('touchend', () => mouse.down = false);
        window.addEventListener('touchmove', (e) => {{ handleInput(e); e.preventDefault(); }}, {{passive: false}});

        function animate() {{
            // Xóa vết cũ chậm hơn một chút để giữ lại ít dấu vết "nghệ thuật"
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            
            if(mouse.down) {{
                // Chỉ bắn ra số lượng hạt theo slider 'spray_density'
                for(let i=0; i<{spray_density}; i++) {{
                    particles.push(new Particle(mouse.x, mouse.y));
                }}
            }}

            for(let i = 0; i < particles.length; i++) {{
                particles[i].update();
                particles[i].draw();
                if(particles[i].alpha <= 0) {{
                    particles.splice(i, 1);
                    i--;
                }}
            }}
            requestAnimationFrame(animate);
        }}

        window.addEventListener('resize', resize);
        resize();
        animate();
    </script>
</body>
</html>
"""

components.html(html_code, height=750)

st.markdown("<h3 style='text-align: center; color: #444;'>Thiết kế bởi Nguyen Thanh Duy</h3>", unsafe_allow_html=True)
