import graphene
import graphql_jwt
from graphene import relay  # Import związany z integracją z Relay
from graphene_django import DjangoObjectType
from graphene import InputObjectType
from filmy.models import Film, ExtraInfo, Ocena, Aktor
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField  # Import związany z integracją z Relay
#
# Typy
#

class FilmType(DjangoObjectType):
    class Meta:
        model = Film
        fields = ("id", "tytul", "rok", "opis", "premiera", "imdb_pkts", "wyswietlany", "einfo", "oceny", "aktor", "owner")

# Definicja typu na potrzeby Relay
class FilmNode(DjangoObjectType):
    class Meta:
        model = Film
        filter_fields = {
            'tytul': ['exact','contains','startswith'],
            'rok': ['exact']
        }
        interfaces = (relay.Node, )


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class ExtraInfoType(DjangoObjectType):
    class Meta:
        model = ExtraInfo
        convert_choices_to_enum = False
        fields = ("id", "czas_trwania", "gatunek", "rezyser", "film", "owner")


class OcenaType(DjangoObjectType):
    class Meta:
        model = Ocena
        fields = "__all__"


class AktorType(DjangoObjectType):
    class Meta:
        model = Aktor
        fields = "__all__"


class Filters(graphene.InputObjectType):
    tytul_zawiera = graphene.String(default_value="")
    rok_mniejszy_od = graphene.Int(default_value=2000)
    nazwisko_aktora = graphene.String(default_value="")


class FilmFilter(InputObjectType):
    tytul_contains = graphene.String(default_value="")
#
# Query
#
class Query(graphene.ObjectType):
    # filmy = graphene.List(FilmType, filters=FilmFilter())
    filmy = DjangoFilterConnectionField(FilmNode)
    # film_wg_id = graphene.Field(FilmType, id=graphene.String())
    film_wg_id = relay.Node.Field(FilmNode)
    extrainfo = graphene.List(ExtraInfoType)
    extrainfo_wg_id = graphene.Field(ExtraInfoType, id=graphene.String())
    oceny = graphene.List(OcenaType)
    oceny_wg_filmu = graphene.List(OcenaType, film_tytul_contains=graphene.String(default_value=""))
    aktorzy = graphene.List(AktorType, filters=Filters())

    # @login_required
    # def resolve_filmy(root, info, filters):
    #     filmy = Film.objects.all()
    #     for f in filmy:
    #         if f.rok < filters.rok_mniejszy_od:
    #             f.stary_nowy_film = "Stary film"
    #         else:
    #             f.stary_nowy_film = "Nowy film"
    #     if len(filters.tytul_zawiera) > 0:
    #         films = Film.objects.filter(tytul__contains=filters.tytul_zawiera)
    #         for f in films:
    #             if f.rok < filters.rok_mniejszy_od:
    #                 f.stary_nowy_film = "Stary film"
    #             else:
    #                 f.stary_nowy_film = "Nowy film"
    #         return films
    #     return filmy
    #
    # def resolve_film_wg_id(root, info, id):
    #     f = Film.objects.get(pk=id)
    #     f.rok2 = int(f.rok) + 10
    #
    #     return f

    def resolve_extrainfo(root, info):
        return ExtraInfo.objects.all()

    def resolve_extrainfo_wg_id(root, info, id):
        einfo = ExtraInfo.objects.get(pk=id)
        return einfo

    def resolve_oceny(root, info):
        return Ocena.objects.all()

    def resolve_oceny_wg_filmu(root, info, film_tytul_contains):
        oceny = Ocena.objects.all()
        if film_tytul_contains is not None:
            o = Ocena.objects.filter(film__tytul__contains=film_tytul_contains)
            return o

        return oceny

    def resolve_aktorzy(root, info, filters):
        aktorzy = Aktor.objects.all()
        if len(filters.nazwisko_aktora) > 0:
            aktor = Aktor.objects.filter(nazwisko__contains=filters.nazwisko_aktora)
            return aktor
        return aktorzy


#
# Mutacje
#


class FilmCreateMutation(graphene.Mutation):
    class Arguments:
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_pkts = graphene.Decimal()
        owner_id = graphene.ID()

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, tytul, opis, rok, imdb_points, owner_id):
        film = Film.objects.create(tytul=tytul, opis=opis, rok=rok, imdb_points=imdb_points, owner_id=owner_id)
        return FilmCreateMutation(film=film)


class FilmUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_pkts = graphene.Decimal()
        premiera = graphene.Date(default_value=None)
        owner_id = graphene.ID()

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, id, tytul, opis, rok, imdb_points, premiera, owner_id):
        film = Film.objects.get(pk=id)
        film.opis = opis
        film.rok = rok
        film.premiera = premiera
        film.imdb_pkts = imdb_points
        film.owner_id = owner_id
        film.save()
        return FilmUpdateMutation(film=film)


class FilmDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    film = graphene.List(FilmType)

    @classmethod
    def mutate(cls, root, info, id):
        film = Film.objects.get(pk=id).delete()
        film = Film.objects.all()
        return FilmDeleteMutation(film=film)

class AktorCreateMutation(graphene.Mutation):
    class Arguments:
        imie = graphene.String(required=True)
        nazwisko = graphene.String(required=True)
        filmy_ids = graphene.List(graphene.Int)
        owner_id = graphene.ID()

    aktor = graphene.Field(AktorType)

    @classmethod
    def mutate(cls, root, info, imie, nazwisko, filmy_ids=None, owner_id=None):
        owner = User.objects.get(id=owner_id) if owner_id else None
        aktor = Aktor(imie=imie, nazwisko=nazwisko, owner=owner)
        aktor.save()
        if filmy_ids:
            filmy = Film.objects.filter(id__in=filmy_ids)
            aktor.filmy.set(filmy)
        return AktorCreateMutation(aktor=aktor)


class AktorDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            aktor = Aktor.objects.get(id=id)
            aktor.delete()
            success = True
        except Aktor.DoesNotExist:
            success = False
        return AktorDeleteMutation(success=success)


class OcenaCreateMutation(graphene.Mutation):
    class Arguments:
        recenzja = graphene.String()
        gwiazdki = graphene.Int()
        film_id = graphene.Int(required=True)
        owner_id = graphene.ID()

    ocena = graphene.Field(OcenaType)

    @classmethod
    def mutate(cls, root, info, film_id, recenzja="", gwiazdki=5, owner_id=None):
        film = Film.objects.get(id=film_id)
        owner = User.objects.get(id=owner_id) if owner_id else None
        ocena = Ocena(recenzja=recenzja, gwiazdki=gwiazdki, film=film, owner=owner)
        ocena.save()
        return OcenaCreateMutation(ocena=ocena)


class Mutation(graphene.ObjectType):
    create_film = FilmCreateMutation.Field()
    update_film = FilmUpdateMutation.Field()
    delete_film = FilmDeleteMutation.Field()
    create_aktor = AktorCreateMutation.Field()
    delete_aktor = AktorDeleteMutation.Field()
    create_ocena = OcenaCreateMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
