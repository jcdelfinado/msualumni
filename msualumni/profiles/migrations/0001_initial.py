# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Religion'
        db.create_table('religion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=54)),
        ))
        db.send_create_signal(u'profiles', ['Religion'])

        # Adding model 'Tribe'
        db.create_table('tribe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'profiles', ['Tribe'])

        # Adding model 'City'
        db.create_table('city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('country', self.gf('django.db.models.fields.CharField')(default='Philippines', max_length=64)),
        ))
        db.send_create_signal(u'profiles', ['City'])

        # Adding unique constraint on 'City', fields ['city', 'province']
        db.create_unique('city', ['city', 'province'])

        # Adding model 'Residence'
        db.create_table('residence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('barangay', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.City'])),
        ))
        db.send_create_signal(u'profiles', ['Residence'])

        # Adding model 'BusinessAddress'
        db.create_table('business_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(default='Unspecified', max_length=64)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.City'])),
        ))
        db.send_create_signal(u'profiles', ['BusinessAddress'])

        # Adding model 'Alum'
        db.create_table('alum', (
            ('alumni_id', self.gf('django.db.models.fields.CharField')(max_length=12, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True, null=True, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('civil_status', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('citizenship', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('tribe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Tribe'], null=True, blank=True)),
            ('religion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Religion'], null=True, blank=True)),
            ('residence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Residence'], null=True, blank=True)),
            ('hometown', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.City'], null=True, blank=True)),
            ('business_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.BusinessAddress'], null=True, blank=True)),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(default='/media/profiles/no-pic.png', max_length=100)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_approved', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'profiles', ['Alum'])

        # Adding model 'Campus'
        db.create_table('campus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'profiles', ['Campus'])

        # Adding model 'College'
        db.create_table('college', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('campus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Campus'])),
        ))
        db.send_create_signal(u'profiles', ['College'])

        # Adding model 'Program'
        db.create_table('program', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'profiles', ['Program'])

        # Adding model 'Major'
        db.create_table('major', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='None', max_length=32)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Program'])),
        ))
        db.send_create_signal(u'profiles', ['Major'])

        # Adding model 'Graduation'
        db.create_table('graduation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alumni', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Alum'])),
            ('major', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Major'])),
            ('college', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.College'], null=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'profiles', ['Graduation'])


    def backwards(self, orm):
        # Removing unique constraint on 'City', fields ['city', 'province']
        db.delete_unique('city', ['city', 'province'])

        # Deleting model 'Religion'
        db.delete_table('religion')

        # Deleting model 'Tribe'
        db.delete_table('tribe')

        # Deleting model 'City'
        db.delete_table('city')

        # Deleting model 'Residence'
        db.delete_table('residence')

        # Deleting model 'BusinessAddress'
        db.delete_table('business_address')

        # Deleting model 'Alum'
        db.delete_table('alum')

        # Deleting model 'Campus'
        db.delete_table('campus')

        # Deleting model 'College'
        db.delete_table('college')

        # Deleting model 'Program'
        db.delete_table('program')

        # Deleting model 'Major'
        db.delete_table('major')

        # Deleting model 'Graduation'
        db.delete_table('graduation')


    models = {
        u'profiles.alum': {
            'Meta': {'object_name': 'Alum', 'db_table': "'alum'"},
            'alumni_id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'business_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.BusinessAddress']", 'null': 'True', 'blank': 'True'}),
            'citizenship': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'civil_status': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.City']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'default': "'/media/profiles/no-pic.png'", 'max_length': '100'}),
            'religion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Religion']", 'null': 'True', 'blank': 'True'}),
            'residence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Residence']", 'null': 'True', 'blank': 'True'}),
            'tribe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Tribe']", 'null': 'True', 'blank': 'True'})
        },
        u'profiles.businessaddress': {
            'Meta': {'object_name': 'BusinessAddress', 'db_table': "'business_address'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.City']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'Unspecified'", 'max_length': '64'})
        },
        u'profiles.campus': {
            'Meta': {'object_name': 'Campus', 'db_table': "'campus'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'profiles.city': {
            'Meta': {'unique_together': "(('city', 'province'),)", 'object_name': 'City', 'db_table': "'city'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'Philippines'", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'profiles.college': {
            'Meta': {'object_name': 'College', 'db_table': "'college'"},
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Campus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'profiles.graduation': {
            'Meta': {'object_name': 'Graduation', 'db_table': "'graduation'"},
            'alumni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Alum']"}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.College']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Major']"}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'profiles.major': {
            'Meta': {'object_name': 'Major', 'db_table': "'major'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '32'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Program']"})
        },
        u'profiles.program': {
            'Meta': {'object_name': 'Program', 'db_table': "'program'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'profiles.religion': {
            'Meta': {'object_name': 'Religion', 'db_table': "'religion'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '54'})
        },
        u'profiles.residence': {
            'Meta': {'object_name': 'Residence', 'db_table': "'residence'"},
            'barangay': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'profiles.tribe': {
            'Meta': {'object_name': 'Tribe', 'db_table': "'tribe'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['profiles']