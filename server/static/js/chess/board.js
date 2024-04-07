class Board extends Dispatcher {
    constructor () {
        super()

        this.boardElement = document.querySelector(".board");
        this.cellsElement = document.querySelector(".cells");
        this.piecesElement = document.querySelector(".pieces");
        this.pieces = [];
        this.selectedCells = [];
        this.selectedPiece = undefined

        this.applied = false;
        this.inversed = false;

        for (let y = 0; y < 8; y++) {
            for (let x = 0; x < 8; x++) {
                let cellElement = document.createElement("div");
                
                cellElement.classList.add("cell");
                cellElement.classList.add(x % 2 ^ y % 2 ? "black" : "white");
                cellElement.onmouseenter = () => {
                    let selectedPiece = this.selectedPiece;

                    if (selectedPiece != undefined) {
                        selectedPiece.phantomPos = [x, y];
                    }
                }

                this.cellsElement.appendChild(cellElement);
            }
        }

        this.boardElement.onmouseup = () => {
            let piece = this.selectedPiece;

            if (piece != undefined) {
                this.downPiece();
            }
        }
        this.boardElement.onmousemove = event => {
            let piece = this.selectedPiece;

            if (piece != undefined) {
                let element = piece.element, boardRect = this.boardElement.getBoundingClientRect();
                let elementRect = element.getBoundingClientRect();

                element.style.top = `${event.clientY - boardRect.top - elementRect.width / 2}px`;
                element.style.left = `${event.clientX - boardRect.left - elementRect.height / 2}px`;
            }
        }
    }

    ipos(pos) {
        let [x, y] = pos;

        if (this.inversed) {
            y = 7 - y;
        }

        return [x, y];
    }

    parsePiece(pieceId) {
        pieceId -= 1;

        return [Math.floor(pieceId / 6), pieceId % 6];
    }

    apply(board) {
        this.applied = true;
        
        for (let y = 0; y < 8; y++) {
            for (let x = 0; x < 8; x++) {
                let iy = this.ipos([x, y])[1], 
                    pieceId = board[iy][x],
                    pieceSide;

                [pieceSide, pieceId] = this.parsePiece(pieceId);

                if (pieceId != -1) {
                    this.setPiece(pieceId, [x, iy], pieceSide);
                }
            }               
        }
    }

    inverse() {
        this.inversed = true;
    }

    inversePiece(piece) {
        return new Piece(piece.id, this.ipos(piece.pos), piece.side);
    }

    getCell(pos) {
        let [x, y] = pos;

        return this.cellsElement.childNodes[y * 8 + x];
    }

    getPiece(pos) {
        let [x, y] = pos;
        
        return this.pieces.find(piece => {
            let [px, py] = piece.pos;
            
            return x == px && y == py;
        });
    }

    setPiece(pieceId, pos, pieceSide) {
        pos = this.ipos(pos);
        
        let piece = new Piece(pieceId, pos, pieceSide);

        piece.element.onmousedown = () => this.upPiece(piece.pos);
        piece.element.onmouseup = event => {
            let piece = this.selectedPiece;

            if (piece != undefined) {
                this.downPiece();
            }
        }
        piece.element.onmouseenter = () => {
            let selectedPiece = this.selectedPiece;

            if (selectedPiece != undefined) {
                selectedPiece.phantomPos = piece.pos;
            }
        }

        this.pieces.push(piece);
        this.piecesElement.appendChild(piece.element);
    }

    movePiece(ppos) {
        let [fpos, tpos] = ppos;

        this.getPiece(fpos).move(tpos);
    }

    select(pos, poss) {
        pos = this.ipos(pos);
        let selectedCell = this.getCell(pos);

        selectedCell.classList.add("blue");
        this.selectedCells.push(selectedCell);
        
        poss.forEach(pos => {
            pos = this.ipos(pos), selectedCell = this.getCell(pos);
            let piece = this.getPiece(pos);
            
            if (piece == undefined) {
                selectedCell.classList.add("green");
            }
            else {
                selectedCell.classList.add("red");
            }

            this.selectedCells.push(selectedCell);
        });
    }

    unselect() {
        this.selectedCells.forEach(selectedCell => {
            let classList = selectedCell.classList;
            
            if (classList.contains("red")) {
                classList.remove("red");
            }
            else if (classList.contains("blue")) {
                classList.remove("blue");
            }
            else if (classList.contains("green")) {
                classList.remove("green");
            }
        });

        this.selectedCells = [];
    }

    canUpPiece(piece) {
        return this.emit("canUpPiece", this.inversePiece(piece));
    }

    upPiece(pos) {
        let piece = this.getPiece(pos);
        
        if (this.selectedPiece != undefined || !this.canUpPiece(piece)) {
            return;
        }

        piece.up();
        this.emit("upPiece", this.inversePiece(piece));

        this.selectedPiece = piece;
    }

    canDownPiece(piece) {
        return this.emit("canDownPiece", [
            this.ipos(piece.phantomPos), this.inversePiece(piece),
        ]);
    }

    downPiece() {
        let piece = this.selectedPiece;
        this.selectedPiece = undefined;

        if (!this.canDownPiece(piece)) {            
            return piece.move(piece.pos);
        }

        this.emit("downPiece", [
            this.ipos(piece.phantomPos), this.inversePiece(piece)
        ]);
        piece.down();
    }

    killPiece(pos) {
        let piece = this.getPiece(pos);
    
        this.pieces = this.pieces.filter(_piece => piece != _piece);
        this.piecesElement.removeChild(piece.element);
    }
}
