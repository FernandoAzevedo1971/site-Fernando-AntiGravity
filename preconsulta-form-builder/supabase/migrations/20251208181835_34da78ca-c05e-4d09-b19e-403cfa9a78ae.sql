-- Create role enum for the application
CREATE TYPE public.app_role AS ENUM ('admin', 'medical_staff');

-- Create user_roles table
CREATE TABLE public.user_roles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    role app_role NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE (user_id, role)
);

-- Enable RLS on user_roles
ALTER TABLE public.user_roles ENABLE ROW LEVEL SECURITY;

-- Create security definer function to check roles (prevents recursive RLS issues)
CREATE OR REPLACE FUNCTION public.has_role(_user_id uuid, _role app_role)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.user_roles
    WHERE user_id = _user_id
      AND role = _role
  )
$$;

-- RLS policy for user_roles: only admins can view all roles
CREATE POLICY "Users can view their own roles"
ON public.user_roles
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Admins can view all roles"
ON public.user_roles
FOR SELECT
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can manage roles"
ON public.user_roles
FOR ALL
TO authenticated
USING (public.has_role(auth.uid(), 'admin'))
WITH CHECK (public.has_role(auth.uid(), 'admin'));

-- Drop existing overly permissive policies on medical_forms
DROP POLICY IF EXISTS "Authenticated users can view forms" ON public.medical_forms;
DROP POLICY IF EXISTS "Authenticated users can update forms" ON public.medical_forms;
DROP POLICY IF EXISTS "Authenticated users can delete forms" ON public.medical_forms;

-- Create new role-based policies for medical_forms
CREATE POLICY "Medical staff can view forms"
ON public.medical_forms
FOR SELECT
TO authenticated
USING (
  public.has_role(auth.uid(), 'medical_staff') 
  OR public.has_role(auth.uid(), 'admin')
);

CREATE POLICY "Medical staff can update forms"
ON public.medical_forms
FOR UPDATE
TO authenticated
USING (
  public.has_role(auth.uid(), 'medical_staff') 
  OR public.has_role(auth.uid(), 'admin')
)
WITH CHECK (
  public.has_role(auth.uid(), 'medical_staff') 
  OR public.has_role(auth.uid(), 'admin')
);

CREATE POLICY "Admins can delete forms"
ON public.medical_forms
FOR DELETE
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));

-- Update audit log policy to use roles
DROP POLICY IF EXISTS "Authenticated users can view audit logs" ON public.medical_forms_audit;

CREATE POLICY "Staff can view audit logs"
ON public.medical_forms_audit
FOR SELECT
TO authenticated
USING (
  public.has_role(auth.uid(), 'medical_staff') 
  OR public.has_role(auth.uid(), 'admin')
);