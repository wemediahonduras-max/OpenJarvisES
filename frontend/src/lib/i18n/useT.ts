import { useCallback } from 'react';
import { useAppStore } from '../store';
import { t, type Locale } from './messages';

export function useT() {
  const locale = useAppStore((s) => s.settings.locale);
  return useCallback(
    (key: string, vars?: Record<string, string | number>) => t(locale, key, vars),
    [locale],
  );
}

export function useLocale(): Locale {
  return useAppStore((s) => s.settings.locale);
}
