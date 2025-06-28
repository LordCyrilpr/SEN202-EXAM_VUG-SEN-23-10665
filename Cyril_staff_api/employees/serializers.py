from rest_framework import serializers
from .models import Manager, Intern, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street_address', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ManagerSerializer(serializers.ModelSerializer):
    """
    Serializer for Manager model.
    Implements encapsulation by making has_company_card read-only.
    """
    full_name = serializers.ReadOnlyField()
    role = serializers.SerializerMethodField()
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Manager
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'hire_date', 'salary', 'is_active', 'created_at', 
            'updated_at', 'full_name', 'role', 'department', 'has_company_card', 'address'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'has_company_card']

    def get_role(self, obj):
        """Get the role using the polymorphic get_role method"""
        return obj.get_role()

    def to_representation(self, instance):
        """
        Override to_representation to protect sensitive data.
        has_company_card is only shown to authorized users.
        """
        data = super().to_representation(instance)
        # In a real application, you would check user permissions here
        # For now, we'll always hide the has_company_card field in the API
        if 'has_company_card' in data:
            data['has_company_card'] = '***PROTECTED***'
        return data


class InternSerializer(serializers.ModelSerializer):
    """
    Serializer for Intern model.
    """
    full_name = serializers.ReadOnlyField()
    role = serializers.SerializerMethodField()
    mentor_name = serializers.ReadOnlyField(source='mentor.full_name')
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Intern
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'hire_date', 'salary', 'is_active', 'created_at', 
            'updated_at', 'full_name', 'role', 'mentor', 'mentor_name', 'internship_end_date', 'address'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_role(self, obj):
        """Get the role using the polymorphic get_role method"""
        return obj.get_role()


class ManagerDetailSerializer(ManagerSerializer):
    """
    Detailed serializer for Manager that includes intern information.
    """
    interns = InternSerializer(many=True, read_only=True)

    class Meta(ManagerSerializer.Meta):
        fields = ManagerSerializer.Meta.fields + ['interns'] 