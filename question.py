from manim import *
import manim
import math
import pathlib
from PIL import Image, ImageFilter
import numpy as np

class MultipleChoice(VMobject):
    def __init__(self,choices: list, true_choice=None, buff_rows=1, buff_cols=0, cols=1, **kwargs):
        super().__init__(**kwargs)

        self.true_choice = true_choice
        self.cols = cols
        self._buff_rows = buff_rows
        self._buff_cols = buff_cols
        self.choices = VGroup()
        for i, choice in enumerate(choices):
            ellipse = Ellipse(width=1.1, height=.8)
            num = MathTex(str(i+1)).move_to(ellipse)
            label = VGroup(num, ellipse)
            choice.next_to(label, LEFT)
            self.choices.add(VGroup(label, choice).arrange(LEFT))
        self._render()
        self.add(self.choices)

    def _render(self):
        self.choices.arrange_in_grid(
            cols=self.cols,
            flow_order="ld",
            col_widths=[config.frame_width/self.cols-1]*self.cols,buff=(self._buff_cols,self._buff_rows),
            col_alignments="r"*self.cols,
        )

    def set_cols(self, cols):
        self.cols = cols
        self._render()
        return self

    def __getitem__(self, index):
        return self.choices[index]

    def __len__(self):
        return len(self.choices)

    def get_true_choice_object(self):
        return self.choices[self.true_choice]

    def get_label(self, index):
        return self.choices[index]

    def indicate_true_choice(self, color=BLACK, fill_color=BLUE_E, border_color=BLUE_E) -> Animation:
        # self.choices[self.true_choice].animate.set_color(color)
        if self.true_choice == None: return
        return (
            DrawBorderThenFill(
                SurroundingRectangle(
                    self.choices[self.true_choice],
                    color=border_color,
                    corner_radius=0.3,
                    fill_color=fill_color,
                    fill_opacity=.3,
                    buff=.2
                )
            ),
            self.choices[self.true_choice].animate.set_color(color),
        )


class Question(VMobject):
    def __init__(self, body, number, level, **kwargs):
        super().__init__(**kwargs)
        self.body = body
        self.number = number
        self.level = level
        self.number_object = Tex(rf"${number}$")
        self.level_object = self._generate_level()
        self.number_level_object = VGroup(self.number_object, self.level_object)
        self.number_level_object.to_corner(UR, buff=.25)
        self.body = body
        self.body.next_to(self.number_level_object,DOWN*1.5).to_edge(RIGHT).shift(LEFT)
        self.add(self.body,self.number_object,self.level_object)


    def _generate_level(self):
        result = VGroup()
        level_whole = math.floor(self.level)
        level_decimal = self.level - level_whole

        for i in range(5):
            opacity = 1 if i < level_whole else 0
            result.add(AnnularSector(outer_radius=.7, inner_radius=.5, angle=PI/3, start_angle=PI/2 + PI/30 + i*2*PI/5, fill_color=BLACK, fill_opacity=opacity, stroke_width=4, stroke_color=BLACK))

        if level_decimal > 0:
            result.add(AnnularSector(outer_radius=.7, inner_radius=.5, angle=PI/3*level_decimal, start_angle=PI/2 + PI/30 + level_whole*2*PI/5, fill_color=BLACK, fill_opacity=1, stroke_width=4, stroke_color=BLACK))

        return result

    def get_level_object(self, strict=True):
        if strict == False:
            return self.level_object
        result = VGroup(self.level_object[0:math.floor(self.level)])
        if len(self.level_object) > 5:
            result.add(self.level_object[-1])
        return result


class Background(VMobject):
    def __init__(self, index, fill_color=BLUE_C, fill_opacity=1, **kwargs):
        super().__init__(**kwargs)

        # self.fill_color = kwargs['fill_color'] if 'fill_color' in kwargs else BLUE_C
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        # self.fill_opacity = kwargs['fill_opacity'] if 'fill_opacity' in kwargs else 1
        self.bg = []

        points = []
        points.append(np.array([-15.7,8.7,0]))
        points.append(np.array([-15.7,-7.7,0]))
        points.append(points[1] + [1,-1,0])
        points.append(np.array([15.7,-8.7,0]))
        points.append(np.array([15.7,7,0]))
        points.append(np.array([1,8,0]))
        points.append(np.array(points[4] + [-4.5,1.5,0]))
        points.append(np.array(points[5] + [4.5,1.5,0]))
        points.append(np.array(points[5] + [-6,-2,0]))
        points.append(np.array(points[0] + [8,-2,0]))
        path = VMobject()
        path.points = np.concatenate([
            Line(points[0],points[1]).points,
            CubicBezier(points[1], points[1] + [0,-.5,0], points[2] + [-.5,0,0], points[2]).points,
            Line(points[2],points[3]).points,
            Line(points[3],points[4]).points,
            CubicBezier(points[4],points[6],points[7],points[5]).points,
            CubicBezier(points[5],points[8],points[9],points[0]).points,
        ])
        rect = Rectangle(width=32, height=18)     
        self.bg.append(
            Exclusion(rect,path, fill_color=self.fill_color, fill_opacity=self.fill_opacity, stroke_width=0)
        )

        self.bg.append(
            VGroup(
                # Rectangle(width=config.frame_width, height=1.3)\
                #     .to_corner(UL, buff=0),
                # Rectangle(width=config.frame_width, height=.5)\
                #     .to_corner(DL, buff=0),
                # Rectangle(width=.5, height=config.frame_height)\
                #     .to_corner(UL, buff=0),
                # Rectangle(width=.5, height=config.frame_height)\
                #     .to_corner(UR, buff=0),
                AnnularSector(inner_radius=0, outer_radius=2.3, angle = PI/2, start_angle=PI).to_corner(UR, buff=0),
                AnnularSector(inner_radius=0, outer_radius=2.3, angle = PI/2, start_angle=3*PI/2).to_corner(UL, buff=0),
                AnnularSector(inner_radius=0, outer_radius=2.3, angle = PI/2, start_angle=0).to_corner(DL, buff=0),
                AnnularSector(inner_radius=0, outer_radius=2.3, angle = PI/2, start_angle=PI/2).to_corner(DR, buff=0),
            ).set_fill(self.fill_color,self.fill_opacity).set_color(fill_color)
        )

        self.add(self.bg[index])


class TransformMatchingTexIndex(AnimationGroup):

    def __init__(self, source, target, transform_index, transform=FadeTransform, copy_source=False, show_indexes=False, **kwargs):

        self._effects = []
        # self._source = source[0]
        # self._target = target[0]
        self._source = source.copy() if copy_source == True else source
        self._target = target
        if show_indexes:
            indexes = VGroup()
            source_copy = self._source.copy().scale(1)
            target_copy = self._target.copy().scale(1)
            rect = RoundedRectangle(corner_radius=0.5, fill_color=GREEN, fill_opacity=1, width=20, height=9)
            rect.z_index = -1
            indexes.add(VGroup(source_copy,self._get_sub_indexes(source_copy)), VGroup(target_copy,self._get_sub_indexes(target_copy)))
            indexes.arrange(DOWN*4)
            indexes.add(rect)
            indexes.z_index = 10000
            self._effects.append(FadeIn(indexes))

        self._source_indexes = []
        self._target_indexes = []
        self.transform = transform

        for index, tuple in enumerate(transform_index):
            if len(tuple) == 2:
                i,j = tuple
                self._transform(i,j, **kwargs)
            elif len(tuple) == 3:
                i,j,num = tuple
                if num == 0:
                    num = len(self._source) - i
                for n in range(num):
                    self._transform(i+n, j+n, **kwargs)
        

        for i in range(len(self._source)):
            if i not in self._source_indexes:
                if copy_source == False:
                    self._effects.append(FadeOut(self._source[i]))
        
        for j in range(len(target)):
            if j not in self._target_indexes:
                self._effects.append(FadeIn(target[j]))

        super().__init__(*self._effects,  **kwargs)

    def _transform(self, i, j, **kwargs):
        if type(i) is list:
            source = VGroup()
            for l in i:
                source.add(self._source[l] if l not in self._source_indexes else self._source[l].copy())
                self._source_indexes.append(l)
        else:
            source = self._source[i] if i not in self._source_indexes else self._source[i].copy()
            self._source_indexes.append(i)

        if type(j) is list:
            target = VGroup()
            for l in j:
                target.add(self._target[l])
                self._target_indexes.append(l)
        else:
            target = self._target[j]
            self._target_indexes.append(j)        

        self._effects.append(self.transform(source,target, **kwargs))


    def _get_sub_indexes(self, tex):
        # tex = tex[0]
        ni = VGroup()
        color = BLACK
        for i in range(len(tex)):
            n = Text(f"{i}",color=color).scale(1)
            n.next_to(tex[i],DOWN,buff=0.01)
            ni.add(n)
        return ni


class WriteLetterByLetter(Succession):
  def __init__(self, mobject, reverse=False, run_time=None, **kwargs):
    self.run_time = .2 if run_time == None else run_time
    self._effects = []
    for object in mobject:
      self._effects.append(Write(object, run_time=self.run_time, **kwargs))
    if reverse == True: self._effects.reverse()
    # self.run_time = run_time/len(mobject) if mobject != None else 1
    super().__init__(Succession(*self._effects),  **kwargs)


def cancel(tex, start, end, buff=.1):
    surect = SurroundingRectangle(
        tex[start:end+1],
        buff=buff
    )
    return Line(surect.get_corner(UR), surect.get_corner(DL))


class Tip(VGroup):
  def __init__(self, header, body, header_fill=BLUE_A, body_fill=ORANGE,  **kwargs):
    super().__init__(**kwargs)
    self.header = header
    self.body = body
    self.header_fill = header_fill
    self.body_fill = body_fill
    self._result = self._render()
    self.add(self._result)

  def _render(self):
    padding = .3
    body_wrap = RoundedRectangle(
      height = self.body.height + padding * 2,
      width = self.body.width + padding * 2,
      corner_radius=.3,
      stroke_width=3,
      color = BLUE_E,
      fill_color = BLUE_A,
      fill_opacity = 1
    )
    header_wrap = VGroup(
      SurroundingRectangle(
        self.header,
        buff=.3,
        corner_radius=.2,
        fill_color = self.header_fill,
        fill_opacity=1,
        stroke_width=2,
        color=BLUE_E
      ),
      self.header
    )
    self.body.move_to(body_wrap, UR).shift(padding*LEFT + padding*DOWN)
    header_wrap.next_to(
      body_wrap, UP, buff=-.2, aligned_edge=RIGHT
    ).shift(LEFT)
    return VGroup(body_wrap, self.body, header_wrap)


class Dim(Rectangle):
  def __init__(self, fill_color=BLACK, fill_opacity=.7, **kwargs):
    width = config.frame_width
    height = config.frame_height
    stroke_width = 0
    super().__init__(
      width=width, height=height, stroke_width = stroke_width,
      fill_color=fill_color, fill_opacity=fill_opacity, **kwargs
    )


class BluredImage(ImageMobject):
    def __init__(self, filename_or_array, blur: float=5, image_mode="RGBA", **kwargs):
      self.blur = blur
      self.image_mode = image_mode

      if isinstance(filename_or_array, (str, pathlib.PurePath)):
        path = get_full_raster_image_path(filename_or_array)
        image = Image.open(path).convert(self.image_mode)
        self.path = path
      else:
        image = Image.fromarray(np.array(filename_or_array))

      self.original_pixel_array = np.array(image)
      image = image.filter(ImageFilter.GaussianBlur(blur))
      pixel_array = np.array(image)

      super().__init__(pixel_array, **kwargs)

    def set_blur(self, blur):
      self.blur = blur
      image = Image.fromarray(self.original_pixel_array)
      image = image.filter(ImageFilter.GaussianBlur(blur))
      self.pixel_array = np.array(image)
      return self


