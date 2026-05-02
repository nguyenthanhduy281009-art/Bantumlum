import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Fluid Spray - Duy", layout="wide")

if 'photo_data' not in st.session_state:
    st.session_state.photo_data = ""

# --- SIDEBAR ---
st.sidebar.title("🔫 Fluid Spray Studio")
uploaded_file = st.sidebar.file_uploader("👤 Tải ảnh người cần 'spray'", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    st.session_state.photo_data = f"data:image/png;base64,{base64.b64encode(file_bytes).decode()}"

# Duy có thể chỉnh độ mạnh nhẹ của tia bắn ở đây
spray_power = st.sidebar.slider("🚀 Lực bắn tia nước", 5, 30, 15)
spray_size = st.sidebar.slider("💧 Kích thước giọt", 2, 15, 6)

if st.sidebar.button("🧹 XÓA SẠCH"):
    st.rerun()

# --- HTML/JS: HIỆU ỨNG BẮN HẠT TRẮNG ĐỤC ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #000; }}
        #bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{st.session_state.photo_data}');
            background-size: contain; background-repeat: no-repeat; background-position: center;
            z-index: -1;
        }}
        canvas {{ position: absolute; top: 0; left: 0; cursor: crosshair; }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <canvas id="canvas"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}

        class Particle {{
            constructor(x, y) {{
                this.x = x;
                this.y = y;
                // Hiệu ứng bắn tóe: Vận tốc ngẫu nhiên theo mọi hướng
                this.vx = (Math.random() - 0.5) * {spray_power};
                this.vy = (Math.random() - 0.5) * {spray_power};
                this.radius = Math.random() * {spray_size} + 1;
                this.alpha = 1;
                this.gravity = 0.2; // Trọng lực làm hạt rơi xuống
            }}

            update() {{
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.alpha -= 0.01; // Mờ dần khi bay
            }}

            draw() {{
                // Màu trắng đục (rgba 255, 255, 255 với độ trong suốt)
                ctx.fillStyle = `rgba(240, 240, 240, ${{this.alpha}})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        function createSpray(e) {{
            const x = e.clientX || (e.touches && e.touches[0].clientX);
            const y = e.clientY || (e.touches && e.touches[0].clientY);
            
            // Mỗi lần click/di chuyển bắn ra nhiều hạt cùng lúc
            for (let i = 0; i < 8; i++) {{
                particles.push(new Particle(x, y));
            }}
        }}

        window.addEventListener('mousedown', (e) => {{
            window.isSpraying = true;
            createSpray(e);
        }});
        window.addEventListener('mouseup', () => window.isSpraying = false);
        window.addEventListener('mousemove', (e) => {{
            if (window.isSpraying) createSpray(e);
        }});
        
        window.addEventListener('touchstart', (e) => {{ 
            window.isSpraying = true; 
            createSpray(e); 
        }}, {{passive: false}});
        window.addEventListener('touchend', () => window.isSpraying = false);
        window.addEventListener('touchmove', (e) => {{
            if (window.isSpraying) {{
                e.preventDefault();
                createSpray(e);
            }}
        }}, {{passive: false}});

        function animate() {{
            // Tạo hiệu ứng vết mờ (trail) để tia nước nhìn mượt hơn
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'; 
            // Lưu ý: Nếu muốn vết bắn dính lại vĩnh viễn, ta không clearRect toàn bộ
            // Ở đây mình chọn clear nhẹ để tạo độ mượt
            
            for (let i = 0; i < particles.length; i++) {{
                particles[i].update();
                particles[i].draw();
                if (particles[i].alpha <= 0) {{
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

components.html(html_code, height=700)

st.markdown("<h2 style='text-align: center; color: white;'>🚀 SPRAY EFFECT BY NGUYEN THANH DUY</h2>", unsafe_allow_html=True)
