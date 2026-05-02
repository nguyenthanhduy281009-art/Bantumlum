import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang rộng toàn màn hình
st.set_page_config(page_title="Fluid Magic - Duy", layout="wide")

# --- GIAO DIỆN ĐIỀU KHIỂN CỦA STREAMLIT ---
st.sidebar.title("🎨 Bảng Điều Khiển")
bg_url = st.sidebar.text_input("Dán link ảnh nền (URL):", placeholder="https://example.com/background.jpg")
p_color = st.sidebar.color_picker("Chọn màu chất lỏng:", "#FF4B4B")
is_random = st.sidebar.checkbox("Sử dụng màu cầu vồng", value=True)
p_power = st.sidebar.slider("Độ mạnh tia nước:", 5, 50, 15)

# --- NHÚNG CODE HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; }}
        #bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{bg_url}');
            background-color: #1a1a1a;
            background-size: cover; background-position: center;
            z-index: -1;
        }}
        canvas {{ display: block; cursor: crosshair; }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <canvas id="canvas"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        class Particle {{
            constructor(x, y, color) {{
                this.x = x;
                this.y = y;
                this.size = Math.random() * 10 + 2;
                this.speedX = Math.random() * 8 - 4;
                this.speedY = Math.random() * 8 - 4;
                this.color = color;
                this.gravity = 0.15;
                this.opacity = 1;
            }}
            update() {{
                this.speedY += this.gravity;
                this.x += this.speedX;
                this.y += this.speedY;
                this.opacity -= 0.015;
            }}
            draw() {{
                ctx.globalAlpha = this.opacity;
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        function spawn(e) {{
            const x = e.touches ? e.touches[0].clientX : e.clientX;
            const y = e.touches ? e.touches[0].clientY : e.clientY;
            for (let i = 0; i < {p_power}; i++) {{
                const color = {str(is_random).lower()} ? `hsl(${{Math.random() * 360}}, 100%, 50%)` : '{p_color}';
                particles.push(new Particle(x, y, color));
            }}
        }}

        window.addEventListener('mousedown', spawn);
        window.addEventListener('mousemove', (e) => {{ if(e.buttons === 1) spawn(e) }});
        window.addEventListener('touchmove', spawn);

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {{
                particles[i].update();
                particles[i].draw();
                if (particles[i].opacity <= 0) {{ particles.splice(i, 1); i--; }}
            }}
            requestAnimationFrame(animate);
        }}
        animate();
    </script>
</body>
</html>
"""

# Hiển thị Game
components.html(html_code, height=600)

# --- CHÂN TRANG SIÊU NỔI BẬT ---
st.markdown(
    f"""
    <div style="text-align: center; padding: 20px; border-radius: 15px; background: #1e1e1e; border: 2px solid #FF4B4B; box-shadow: 0 0 15px #FF4B4B; margin-top: 20px;">
        <h2 style="color: #FF4B4B; margin: 0; font-family: sans-serif;">🚀 POWERED BY</h2>
        <h1 style="color: #FFFFFF; margin: 5px 0; font-size: 40px; text-shadow: 0 0 10px #FF4B4B;">NGUYEN THANH DUY</h1>
        <p style="color: #AAAAAA;">Dữ liệu & Logic cập nhật Meta 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)
