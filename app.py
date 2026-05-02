import streamlit as st
import streamlit.components.v1 as components
import base64

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Paint Master - Duy", layout="wide", initial_sidebar_state="expanded")

# --- CSS TÙY CHỈNH GIAO DIỆN ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stSidebarUserContent"] { padding-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 20px; background: #FF4B4B; color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ĐIỀU KHIỂN ---
st.sidebar.title("🎮 Paint Studio")
uploaded_file = st.sidebar.file_uploader("🖼️ Tải ảnh nền từ bộ sưu tập", type=["jpg", "jpeg", "png"])

bg_data = ""
if uploaded_file:
    file_bytes = uploaded_file.read()
    bg_data = f"data:image/png;base64,{base64.b64encode(file_bytes).decode()}"

p_color = st.sidebar.color_picker("🎨 Màu sơn", "#00F2FF")
is_rainbow = st.sidebar.checkbox("🌈 Chế độ cầu vồng", value=True)
p_size = st.sidebar.slider("💧 Kích thước giọt", 5, 30, 15)
p_power = st.sidebar.slider("🔫 Áp lực phun", 10, 100, 30)

# Nút Reset sử dụng session_state để reload component
if st.sidebar.button("🧹 RESET MÀN HÌNH"):
    st.rerun()

# --- CODE HTML/JS VỚI HIỆU ỨNG DÍNH SƠN ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #1a1a1a; }}
        #container {{ position: relative; width: 100vw; height: 100vh; }}
        canvas {{ position: absolute; top: 0; left: 0; }}
        #bg {{ 
            position: fixed; width: 100%; height: 100%; 
            background-image: url('{bg_data}');
            background-size: cover; background-position: center; z-index: -1;
        }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <div id="container">
        <!-- Canvas chứa các vết sơn đã dính -->
        <canvas id="paintCanvas"></canvas>
        <!-- Canvas chứa các tia nước đang bay -->
        <canvas id="fluidCanvas"></canvas>
    </div>

    <script>
        const pCanvas = document.getElementById('paintCanvas');
        const fCanvas = document.getElementById('fluidCanvas');
        const pCtx = pCanvas.getContext('2d');
        const fCtx = fCanvas.getContext('2d');

        let width, height;
        let particles = [];

        function resize() {{
            width = window.innerWidth;
            height = window.innerHeight;
            pCanvas.width = fCanvas.width = width;
            pCanvas.height = fCanvas.height = height;
        }}
        window.addEventListener('resize', resize);
        resize();

        class Drop {{
            constructor(x, y, color, size) {{
                this.x = x;
                this.y = y;
                this.size = size * (Math.random() * 0.5 + 0.5);
                this.color = color;
                // Tạo vận tốc hướng tâm (phun tỏa ra)
                const angle = Math.random() * Math.PI * 2;
                const force = Math.random() * {p_power / 5};
                this.vx = Math.cos(angle) * force;
                this.vy = Math.sin(angle) * force;
                this.gravity = 0.2;
                this.life = 1;
            }}

            update() {{
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.life -= 0.02;

                // Khi giọt nước "rơi" xuống mặt phẳng (life thấp), nó dính vào pCanvas
                if (this.life < 0.1 || this.size < 1) {{
                    this.stick();
                    return false;
                }}
                return true;
            }}

            stick() {{
                pCtx.globalAlpha = 0.8;
                pCtx.fillStyle = this.color;
                pCtx.filter = 'blur(1px)'; // Làm vết sơn thật hơn
                pCtx.beginPath();
                // Vẽ vết sơn loang lổ ngẫu nhiên
                pCtx.arc(this.x, this.y, this.size * 1.5, 0, Math.PI * 2);
                pCtx.fill();
            }}

            draw() {{
                fCtx.globalAlpha = this.life;
                fCtx.fillStyle = this.color;
                fCtx.beginPath();
                fCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                fCtx.fill();
            }}
        }}

        function emit(e) {{
            const x = e.touches ? e.touches[0].clientX : e.clientX;
            const y = e.touches ? e.touches[0].clientY : e.clientY;
            const color = {str(is_rainbow).lower()} ? `hsl(${{Math.random() * 360}}, 80%, 60%)` : '{p_color}';
            
            for(let i=0; i<5; i++) {{
                particles.push(new Drop(x, y, color, {p_size}));
            }}
        }}

        window.addEventListener('mousedown', emit);
        window.addEventListener('mousemove', (e) => {{ if(e.buttons === 1) emit(e); }});
        window.addEventListener('touchmove', emit);

        function frame() {{
            fCtx.clearRect(0, 0, width, height);
            for(let i=0; i<particles.length; i++) {{
                if(!particles[i].update()) {{
                    particles.splice(i, 1);
                    i--;
                } else {{
                    particles[i].draw();
                }}
            }}
            requestAnimationFrame(frame);
        }}
        frame();
    </script>
</body>
</html>
"""

# Hiển thị Game
components.html(html_code, height=700)

# --- FOOTER SIÊU CẤP ---
st.markdown(f"""
    <div style="text-align: center; padding: 30px; border-radius: 20px; background: linear-gradient(145deg, #1e1e1e, #252525); border: 3px solid #FF4B4B; box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.5);">
        <h2 style="color: #FF4B4B; margin: 0; letter-spacing: 2px;">🚀 POWERED BY</h2>
        <h1 style="color: #FFFFFF; margin: 10px 0; font-size: 50px; text-shadow: 0 0 10px #FF4B4B;">NGUYEN THANH DUY</h1>
        <p style="color: #00FF00; font-weight: bold;">🛡️ Realistic Fluid Simulation - Meta 2026</p>
    </div>
    """, unsafe_allow_html=True)
