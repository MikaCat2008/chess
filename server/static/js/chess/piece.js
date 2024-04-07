class Piece {
    constructor (id, pos, side) {
        this.id = id;
        this.pos = pos;
        this.side = side
        this.element = document.createElement("div");
        this.phantomPos = undefined;

        let [x, y] = pos;

        this.element.classList.add("piece");
        this.element.innerHTML = `<img src="static/media/${6 * side + id}.png" draggable="false" />`;
        this.element.style.top = `${12.5 * y}%`;
        this.element.style.left = `${12.5 * x}%`;
    }

    move(pos) {
        let [x, y] = pos;

        this.pos = pos;
        this.element.style.top = `${12.5 * y}%`;
        this.element.style.left = `${12.5 * x}%`;

        if (this.element.classList.contains("free")) {
            this.element.classList.remove("free");
        }
    }

    up() {
        this.element.classList.add("free");
    }

    down() {
        let [phx, phy] = this.phantomPos;

        this.element.style.top = `${12.5 * phy}%`;
        this.element.style.left = `${12.5 * phx}%`;
        this.element.classList.remove("free");

        this.pos = this.phantomPos;
    }
}
