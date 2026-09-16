from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    """Singleton-style model holding the hero / about-me info (usually just one row)."""
    full_name = models.CharField(max_length=100)
    role_title = models.CharField(max_length=150, help_text="e.g. 'web designer'")
    typewriter_roles = models.CharField(
        max_length=255,
        help_text="Comma separated roles for the typewriter effect, e.g. 'developer, creator, gamer'",
    )
    tagline = models.CharField(max_length=255, blank=True)
    is_available_for_freelance = models.BooleanField(default=True)
    hero_illustration = models.ImageField(upload_to="profile/", blank=True, null=True)
    about_text = models.TextField(blank=True)
    about_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    location = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    def get_typewriter_list(self):
        return [w.strip() for w in self.typewriter_roles.split(",") if w.strip()]


class HeroStat(models.Model):
    """The three mini-stats under the hero text (Projects shipped, yrs building, etc.)."""
    profile = models.ForeignKey(Profile, related_name="stats", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    target_value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g. '+', 'yr', '%'")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.target_value}{self.suffix} - {self.label}"


class NowBuilding(models.Model):
    """'Now building' section. Only the active one is shown on the page."""
    profile = models.ForeignKey(Profile, related_name="now_building", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    status = models.CharField(max_length=50, default="In progress")
    description = models.TextField()
    progress_percent = models.PositiveSmallIntegerField(default=0)
    stack = models.CharField(max_length=150, help_text="e.g. 'HTML · CSS · JS'")
    next_note = models.CharField(max_length=150, blank=True, help_text="e.g. 'Next: case study polish'")
    image = models.ImageField(upload_to="now_building/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Now building"

    def __str__(self):
        return self.title


class Quote(models.Model):
    text = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'"{self.text}" - {self.author}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    image = models.ImageField(upload_to="projects/")
    description = models.TextField(help_text="Short summary shown on the project card")
    overview = models.TextField(
        blank=True, help_text="Longer write-up shown in the '#overview' section of the detail page"
    )
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    live_url = models.URLField(blank=True)
    cached_url = models.URLField(blank=True)

    # Detail-page meta row
    role = models.CharField(max_length=100, blank=True, help_text="e.g. 'Solo developer'")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. '~2 weeks'")
    status = models.CharField(max_length=100, blank=True, help_text="e.g. 'Archived', 'Live'")
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})


class ProjectFeature(models.Model):
    """One card in the '#key-features' grid on the project detail page."""
    project = models.ForeignKey(Project, related_name="features", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon_svg = models.TextField(
        blank=True,
        help_text="Inner SVG markup only (paths/rects), no outer <svg> tag. Rendered inside a 24x24 viewBox.",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ProjectGalleryImage(models.Model):
    """One image in the '#gallery' section on the project detail page."""
    project = models.ForeignKey(Project, related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} - image {self.order}"


class SkillCategory(models.Model):
    """e.g. Languages, Frameworks, Databases, Other, Tools."""
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField(default=0)
    show_as_bars = models.BooleanField(
        default=False,
        help_text="Checked = items render as progress bars (like Languages). Unchecked = tag cloud.",
    )

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class SkillItem(models.Model):
    category = models.ForeignKey(SkillCategory, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    proficiency_percent = models.PositiveSmallIntegerField(
        default=0, help_text="Only used when the category shows bars",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ContactLink(models.Model):
    label = models.CharField(max_length=100, help_text="e.g. 'Discord', 'Email'")
    icon = models.ImageField(upload_to="icons/", blank=True, null=True)
    value = models.CharField(max_length=150, help_text="e.g. '!Elias#3519' or 'elias@elias.me'")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactMessage(models.Model):
    """Submissions coming from the '#send-message' contact form."""
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=150, help_text="Email or phone number")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d %H:%M}"


class VisitRequest(models.Model):
    """Phone numbers submitted by visitors who want to arrange a meeting."""
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Visit request"
        verbose_name_plural = "Visit requests"

    def __str__(self):
        return f"{self.phone} - {self.created_at:%Y-%m-%d %H:%M}"