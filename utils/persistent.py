from hashlib import sha256
import os, struct


class CorruptedFileError(Exception):
    pass


class Configs:
    def __init__(self, file:str):
        self.__color:int = 0
        self.__width:int = 640
        self.__height:int = 480
        self.__res_index:int = 0 # 640 x 480
        self.__sound:bool = True
        self.__save:bool = False
        self.__difficulty_index:int = 0 # Fácil
        self.__difficulties:list[tuple[str, int, int]] = []
        self.__resolutions = ((640, 480), (800, 600), (960, 720), (1024, 768))
        self.__filename = file

        if os.path.exists(file):
            with open(file, 'rb') as f:
                hash_ = f.read(32)
                content = f.read()

                if hash_ != sha256(content).digest():
                    raise CorruptedFileError("Arquivo de salvamento inválido ou corrompido")
                
                self.__color = int(content[0])
                self.__res_index = int(content[1])
                if self.__res_index == 255:
                    self.width = struct.unpack('H', content[2:4])[0]
                    #self.__height = 3*self.__width//4
                else:
                    self.__width, self.__height = self.__resolutions[self.__res_index]
                
                vf = int(content[4])
                self.__sound = bool(vf&1)
                self.__save = bool(vf&2)
                self.__difficulty_index = int(content[5])

                for df in content[6:].split(b'\x00\x01'):
                    if not df:
                        break
                    self.__difficulties.append((df[:-3].decode("utf-8"), *struct.unpack('HB', df[-3:])[::-1]))

        else:
            self.save()
    
    def __repr__(self):
        return f"Config(color={self.__color}, width={self.__width}, height={self.__height}, resolution={self.__res_index}, "+\
            f"sound={self.__sound}, autosave={self.__save}, difficulty={self.__difficulty_index}, custom_difficulties={self.__difficulties})"

    def save(self):
        data:list[int] = [self.__color, self.__res_index]

        if self.__res_index == 255:
            data.extend(struct.pack('H', self.__width))
        else:
            data.extend((0, 0))
        
        vf = 0
        if self.__sound:
            vf |= 1 

        if self.__save:
            vf |= 2

        data.extend((vf, self.__difficulty_index))
        diffs = b''
        for name, side, nmine in self.__difficulties:
            name = name.encode('utf-8')
            diffs += name+struct.pack('HB', nmine, side)+b'\x00\x01'
        
        with open(self.__filename, 'wb') as file:
            diffs = diffs[:-2]
            save = bytes(data)+diffs
            hash_ = sha256(save).digest()
            file.write(hash_+save)
    
    @property
    def color(self) -> int:
        return self.__color
    
    @color.setter
    def color(self, value:int):
        if not isinstance(value, int):
            raise ValueError("\"color\" deve ser um inteiro")
            
        if value < 0 or value > 4:
            raise ValueError("\"color\" deve estar dentro do intervalo 0 <= color <= 4")
        
        self.__color = value
    
    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def width(self, value:int):
        if not isinstance(value, int):
            raise ValueError("\"width\" deve ser um inteiro")
            
        if value < 0 or value > 65535:
            raise ValueError("\"width\" deve estar dentro do intervalo 0 <= width <= 65535")
        
        self.__width = value
        self.__height = 3*value//4
        self.__res_index = 255

    @property
    def height(self) -> int:
        return self.__height
    
    @height.setter
    def height(self, value:int):
        if not isinstance(value, int):
            raise ValueError("\"height\" deve ser um inteiro")
        
        self.width = 4*value//3
        self.__height = value
    
    @property
    def resolution(self) -> tuple[int, int]:
        return (self.__width, self.__height)
    
    @property
    def default_resolutions(self) -> tuple:
        return self.__resolutions

    @property
    def sound_enabled(self) -> bool:
        return self.__sound
    
    @sound_enabled.setter
    def sound_enabled(self, value:bool):
        self.__sound = bool(value)

    @property
    def auto_save_enabled(self) -> bool:
        return self.__save
    
    @auto_save_enabled.setter
    def auto_save_enabled(self, value:bool):
        self.__save = bool(value)

    def set_resolution_index(self, index:int):
        if index != 255:
            self.__resolutions[index]
        
        self.__res_index = index
        self.__width, self.__height = self.__resolutions[index]
    
    @property
    def custom_difficulties(self) -> list[tuple[str, int, int]]:
        return self.__difficulties.copy()
    
    @property
    def current_difficulty(self) -> int:
        return self.__difficulty_index

    def set_difficulty(self, index:int):
        if not isinstance(index, int) or index < 0:
            raise ValueError("O atributo \"index\" deve ser um inteiro maior que 0")

        if index in (0, 1, 2):
            self.__difficulty_index = index
        
        else:
            self.__difficulties[index-3]
            self.__difficulty_index = index
    
    def append_difficulty(self, name:str, side:int, nmines:int) -> int:
        for nm, s, n in self.__difficulties:
            if (s, n) == (side, nmines):
                raise Exception(f"A dificuldade {nm} já tem o mesmo lado e número de minas")

        d = (name, side, nmines)
        self.__difficulties.append(d)
        self.__difficulties.sort()
        
        return self.__difficulties.index(d)+3
    
    def remove_difficulty(self, index:int):
        self.__difficulties.pop(index)


class History:
    def __init__(self, file:str):
        try:
            self.__file = open(file, 'r+b')
            hash_ = self.__file.read(32)

            if self.__calc_hash() != hash_:
                raise CorruptedFileError("Arquivo de salvamento inválido ou corrompido")

        except FileNotFoundError:
            self.__file = open(file, 'w+b')
            self.__file.write(self.__calc_hash())
    
    def __del__(self):
        self.__file.close()
    
    def __iter__(self):
        self.__file.seek(32)
        return self
    
    def __next__(self) -> list[int|str|bool]:
        data = self.__file.read(22)
        if len(data) != 22:
            raise StopIteration

        return list(struct.unpack('<IQIBHH?', data))
    
    def __calc_hash(self) -> bytes:
        seek_bkp = self.__file.seek(0, 1)
        self.__file.seek(32)

        hc = sha256()
        for c in iter(lambda: self.__file.read(1024), b''):
            hc.update(c)

        self.__file.seek(seek_bkp)
        return hc.digest()
    
    def add(self, *args:int|bool):
        'Valores adicionados na seguinte ordem: pontuação, momento da partida (timestamp), duração, dificuldade, número de minas, minas marcadas e vitória'

        seek_bkp = self.__file.seek(0, 1)
        self.__file.seek(0, 2)
        self.__file.write(struct.pack('<IQIBHH?', *args))
        self.__file.seek(0)
        self.__file.write(self.__calc_hash())
        self.__file.seek(seek_bkp)
