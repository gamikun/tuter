from PIL import Image, ImageDraw, ImageFont
from operator import attrgetter, itemgetter

class Project:
    def __init__(self, animation=None, size=(1920, 1080),
                 visible_items=10, time_scale='year',
                 time_range=(2000, 2020),
                 background_color=(255, 255, 255, 255),
                 font=None, use_icons=True, icons_size=48):
        self.items = []
        self.animation = animation
        self.size = size
        self.visible_items = 10
        self.time_scale = time_scale
        self.time_range = time_range
        self.background_color = background_color
        self.data_padding = Padding(all=64)
        self.space_between = icons_size
        
        self.use_icons = use_icons
        self.icons_size = icons_size

        self.font = ImageFont.truetype('din.ttf', 40)

        self.item_label_length = 0
        self.longest_item = ''

        self.highest_value = 0

    def add_item(self, **kwargs):
        item = Item(**kwargs)
        self.items.append(item)

        if len(item.label) > self.item_label_length:
            self.item_label_length = len(item.label)
            self.longest_item = item

        # Find highest value
        for key, value in item.values.items():
            if value > self.highest_value:
                self.highest_value = value

    def generate_image(self, step=None, time=0):
        assert isinstance(step, tuple)

        from_step, to_step = step
        w, h = self.size
        image = Image.new('RGBA', self.size)
        draw = ImageDraw.Draw(image)
        dpad = self.data_padding

        right_width, right_height = draw.textsize(
            str(self.highest_value),
            font=self.font
        )

        container_height = h - dpad.bottom - dpad.top
        space_between = (len(self.items) - 1) * self.space_between
        rows_height = container_height - space_between
        row_height = rows_height / len(self.items)

        # Calculate the max width of an icon
        max_icon_width = 0
        for index, item in enumerate(self.items):
            icon_width = item.image_width_for_height(row_height)
            if icon_width > max_icon_width:
                max_icon_width = icon_width

        label_width, label_height = draw.textsize(
            self.longest_item.label,
            font=self.font
        )
        label_width += 32

        draw.rectangle([(0, 0), (w, h)], fill=self.background_color)

        start = sorted([x for x in self.items],
            key=lambda k: k.values[from_step],
            reverse=True
        )
        end = sorted([x for x in self.items],
            key=lambda k: k.values[to_step],
            reverse=True 
        )

        max_from = start[0].values[from_step]
        max_to = end[0].values[to_step]
        
        if max_to > max_from:
            max_resolution = max_to - max_from
            max_value = max_from + max_resolution * time
        else:
            max_resolution = max_from - max_to
            max_value = max_to + max_resolution * (1.0 - time)

        max_width = w - dpad.right - dpad.left 
        max_width -= right_width + 64 + max_icon_width
        scale = max_width / float(max_value)

        for index, item in enumerate(start):
            move_to_index = None

            for to_index, to_item in enumerate(end):
                if to_item == item:
                    move_to_index = to_index
                    break

            x = 0 + dpad.left + label_width
            low_y = index * row_height + dpad.top
            low_y += self.space_between * index if index > 0 else 0
            height = row_height

            high_y = move_to_index * row_height + dpad.top
            high_y += self.space_between * move_to_index \
                     if move_to_index > 0 else 0
            distance_y = high_y - low_y

            y = low_y + (distance_y * time)
            #y += self.space_between * index if index > 0 else 0

            value_from = item.values[from_step]
            value_to = end[move_to_index].values[to_step]

            if value_to > value_from:
                value_resolution = value_to - value_from
                value = value_from + value_resolution * time
            else:
                value_resolution = value_from - value_to
                value = value_to + value_resolution * (1.0 - time)
            
            x2 = x + scale * value - label_width
            y2 = height + y

            draw.rectangle([(x, y), (x2, y2)],
                fill=item.color
            )

            _, icon_h = item.image.size
            icon_width = item.image_width_for_height(row_height)
            icon_x = x2 + 32

            value_text = "{}".format(int(value))
            value_width, value_height = draw.textsize(
                value_text,
                font=self.font
            )
            value_x = icon_x + icon_width + 32
            value_cy = (row_height / float(2)) \
                     - (value_height / float(2)) \
                     + y

            draw.text(
                (value_x, value_cy),
                value_text,
                fill=(0, 0, 0, 255),
                font=self.font
            )

            icon_image = item.image.resize((icon_width, int(row_height)))

            image.alpha_composite(icon_image,
                dest=(int(icon_x), int(y)),
            )

            lw, lh = draw.textsize(item.label, font=self.font)
            lx = dpad.left + label_width - lw - 32

            draw.text(
                (lx, value_cy),
                item.label,
                fill=(0, 0, 0, 255),
                font=self.font
            )

        return image



class AnimationsParameters:
    def __init__(self):
        self.framerate = 60
        self.interval = 1 # seconds


class Item(object):
    __slots__ = ['id', 'values', 'label', 'color', 'image']

    def __init__(self, **kwargs):
        for k in self.__slots__:
            setattr(self, k, kwargs.get(k, None))

    def image_width_for_height(self, height):
        if isinstance(self.image, Image.Image):
            w, h = self.image.size
            return int(height * (w / h))
        else:
            raise TypeError('Not image provided')


class Rect(object):
    __slots__ = ['x', 'y', 'width', 'height']

    def __init__(self, x=0, y=0, width=10, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Padding(object):
    __slots__ = ['left', 'top', 'right', 'bottom']

    def __init__(self, left=16, right=16, top=16, bottom=16, all=None):
        if all is not None:
            self.left = all
            self.right = all
            self.bottom = all
            self.top = all
        else:
            self.left = left
            self.right = right
            self.bottom = bottom
            self.top = top