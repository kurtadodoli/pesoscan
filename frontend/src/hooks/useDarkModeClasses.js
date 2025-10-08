import { useDarkMode } from '../contexts/DarkModeContext';

export const useDarkModeClasses = () => {
  const { isDarkMode } = useDarkMode();
  
  const getPageClasses = (additionalClasses = '') => {
    const baseClasses = 'page-container';
    return `${baseClasses} ${additionalClasses}`.trim();
  };
  
  const getSectionClasses = (isAlternate = false, additionalClasses = '') => {
    const baseClasses = isAlternate ? 'section-alt' : 'section';
    return `${baseClasses} ${additionalClasses}`.trim();
  };
  
  const getCardClasses = (additionalClasses = '') => {
    const baseClasses = 'dark-card';
    return `${baseClasses} ${additionalClasses}`.trim();
  };
  
  const getTextClasses = (type = 'primary', additionalClasses = '') => {
    const baseClasses = `text-${type}`;
    return `${baseClasses} ${additionalClasses}`.trim();
  };
  
  return {
    isDarkMode,
    getPageClasses,
    getSectionClasses,
    getCardClasses,
    getTextClasses
  };
};