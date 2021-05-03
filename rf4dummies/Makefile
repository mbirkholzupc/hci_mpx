.PHONY: po mo

po:
	xgettext -Lpython --output=messages.pot main.py appdesign.kv reference.kv
	msgmerge --update --no-fuzzy-matching --backup=off locales/en/LC_MESSAGES/en.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off locales/es/LC_MESSAGES/es.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off locales/ca/LC_MESSAGES/ca.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off locales/fr/LC_MESSAGES/fr.po messages.pot

mo:
	msgfmt -c -o locales/en/LC_MESSAGES/base.mo locales/en/LC_MESSAGES/en.po
	msgfmt -c -o locales/es/LC_MESSAGES/base.mo locales/es/LC_MESSAGES/es.po
	msgfmt -c -o locales/ca/LC_MESSAGES/base.mo locales/ca/LC_MESSAGES/ca.po
	msgfmt -c -o locales/fr/LC_MESSAGES/base.mo locales/fr/LC_MESSAGES/fr.po