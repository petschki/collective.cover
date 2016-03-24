import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.widgets')
except pkg_resources.DistributionNotFound:
    pass
else:
    from Acquisition import aq_parent
    from Products.CMFCore.utils import getToolByName
    from plone.app.widgets.base import dict_merge
    from plone.app.widgets.dx import RichTextWidget
    from plone.app.widgets.utils import get_tinymce_options
    from z3c.form.interfaces import IFieldWidget, IFormLayer
    from z3c.form.util import getSpecification
    from z3c.form.widget import FieldWidget
    from zope.component import adapter
    from zope.interface import implementer

    from ..tiles.richtext import IRichTextTile


    class TileRichTextWidget(RichTextWidget):
        """ """

        def _base_args(self):
            args = {
                'pattern': self.pattern,
                'pattern_options': self.pattern_options.copy(),
            }
            context = aq_parent(self.wrapped_context())
            args['name'] = self.name
            properties = getToolByName(context, 'portal_properties')
            charset = properties.site_properties.getProperty('default_charset',
                                                             'utf-8')
            value = self.value and self.value.raw_encoded or ''
            args['value'] = (self.request.get(
                self.field.getName(), value)).decode(charset)

            args.setdefault('pattern_options', {})
            merged = dict_merge(get_tinymce_options(context, self.field, self.request),  # noqa
                                args['pattern_options'])
            args['pattern_options'] = merged

            return args


    @adapter(getSpecification(IRichTextTile['text']), IFormLayer)
    @implementer(IFieldWidget)
    def TileRichTextFieldWidget(field, request):
        return FieldWidget(field, TileRichTextWidget(request))
