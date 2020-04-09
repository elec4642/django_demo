from django.db import models

# Create your models here.

class Site(models.Model):
    site_status_choice = (
        (1, 'MSL Completed'),
        (2, 'Cluster Finalization Completed'),
        (3, 'Site Survey Completed'),
        (4, 'Site Survey Review Completed'),
        (5, 'STAD Lockdown Completed'),
        (6, 'DC6 Consultation Completed'),
        (7, 'Site Construction Completed'),
        (8, 'Site Integration and RFI Completed'),
        (9, 'Regulatory Fulfillment Completed'),
        (10, 'SSV Completed')
    )

    site_id = models.CharField(max_length=16, unique=True, verbose_name='Site ID')
    site_name = models.CharField(max_length=64, unique=True, verbose_name='Site Name')
    site_lat = models.FloatField(verbose_name='Latitude')
    site_long = models.FloatField(verbose_name='Longitude')
    site_cluster = models.CharField(max_length=64, verbose_name="Cluster")
    site_state = models.CharField(max_length=32, verbose_name='State')
    site_pole_owner = models.CharField(max_length=64, verbose_name='Pole Owner')
    site_pole_id = models.CharField(max_length=64, unique=True, verbose_name='Pole ID')
    site_rfnsa_id = models.CharField(max_length=12, unique=True, null=True, verbose_name='RFNSA ID')
    site_acma_id = models.CharField(max_length=12, unique=True, null=True, verbose_name='ACMA ID')
    site_status = models.SmallIntegerField(choices=site_status_choice, default=1, verbose_name='Current Status')
    site_last_end_date = models.DateField(null=True, verbose_name='Last milestone date')

    def __str__(self):
        return self.site_id

    class Meta:
        verbose_name = 'SiteBasicData'
        verbose_name_plural = 'SiteBasicData'
        ordering = ['site_id']
        db_table = 'site_basic'

