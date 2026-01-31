import { useEffect, useRef, useCallback } from 'react';

const STORAGE_KEY = 'medical_form_autosave';
const DEBOUNCE_DELAY = 500; // 500ms debounce

interface AutoSaveOptions<T> {
    data: T;
    onRestore?: (data: T) => void;
}

interface AutoSaveReturn {
    lastSaved: Date | null;
    clearSaved: () => void;
    hasRestoredData: boolean;
}

export function useAutoSave<T>(options: AutoSaveOptions<T>): AutoSaveReturn {
    const { data, onRestore } = options;
    const lastSaved = useRef<Date | null>(null);
    const hasRestoredData = useRef(false);
    const timeoutRef = useRef<NodeJS.Timeout>();

    // Load saved data on mount
    useEffect(() => {
        const savedData = localStorage.getItem(STORAGE_KEY);
        if (savedData && onRestore) {
            try {
                const parsed = JSON.parse(savedData);
                if (parsed.data) {
                    onRestore(parsed.data);
                    lastSaved.current = new Date(parsed.timestamp);
                    hasRestoredData.current = true;
                    console.log('[AutoSave] Restored data from:', new Date(parsed.timestamp));
                }
            } catch (error) {
                console.error('[AutoSave] Error restoring data:', error);
                localStorage.removeItem(STORAGE_KEY);
            }
        }
    }, [onRestore]);

    // Save data with debounce
    useEffect(() => {
        // Clear existing timeout
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        // Don't save if data is empty/initial (to avoid overwriting with empty data)
        const isEmptyData = !data || (typeof data === 'object' && Object.keys(data).length === 0);
        if (isEmptyData) {
            return;
        }

        // Set new timeout for debounced save
        timeoutRef.current = setTimeout(() => {
            try {
                const savePayload = {
                    data,
                    timestamp: new Date().toISOString(),
                };
                localStorage.setItem(STORAGE_KEY, JSON.stringify(savePayload));
                lastSaved.current = new Date();
                console.log('[AutoSave] Data saved at:', lastSaved.current);
            } catch (error) {
                console.error('[AutoSave] Error saving data:', error);
            }
        }, DEBOUNCE_DELAY);

        // Cleanup on unmount
        return () => {
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
        };
    }, [data]);

    // Clear saved data
    const clearSaved = useCallback(() => {
        localStorage.removeItem(STORAGE_KEY);
        lastSaved.current = null;
        hasRestoredData.current = false;
        console.log('[AutoSave] Cleared saved data');
    }, []);

    return {
        lastSaved: lastSaved.current,
        clearSaved,
        hasRestoredData: hasRestoredData.current,
    };
}
